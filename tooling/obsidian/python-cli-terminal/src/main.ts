import "../styles.css";

import { execFile } from "node:child_process";
import path from "node:path";
import { promisify } from "node:util";

import { FitAddon } from "@xterm/addon-fit";
import { Terminal } from "@xterm/xterm";
import {
  FileSystemAdapter,
  FileView,
  Modal,
  Plugin,
  PluginSettingTab,
  Setting,
  TFile,
  type App,
  type Menu,
  type TAbstractFile,
  type WorkspaceLeaf,
} from "obsidian";

import { AnalysisService } from "./analysis-service";
import { complete, type CompletionResult } from "./completions";
import { findProjectRoot } from "./resolver";
import { TerminalManager, type TerminalSession } from "./terminal-manager";
import type { CliAdapter, CliAnalysis, Suggestion, ValueProvider } from "./types";

const VIEW_TYPE = "mud-python-cli-terminal-view";
const execFileAsync = promisify(execFile);

interface PluginSettings {
  pythonExecutable: string;
  shellExecutable: string;
  nodeExecutable: string;
  commandHistory: Record<string, string[]>;
  confirmedProjects: Record<string, string>;
}

const DEFAULT_SETTINGS: PluginSettings = {
  pythonExecutable: "python",
  shellExecutable: "pwsh.exe",
  nodeExecutable: "node.exe",
  commandHistory: {},
  confirmedProjects: {},
};

function isPythonFile(file: TAbstractFile): file is TFile {
  return file instanceof TFile && file.extension.toLocaleLowerCase() === "py";
}

async function pythonVersion(executable: string): Promise<string> {
  const { stdout, stderr } = await execFileAsync(executable, ["--version"], {
    windowsHide: true,
    timeout: 3_000,
  });
  return `${stdout}${stderr}`.trim();
}

function versionAtLeast(actual: string, minimum: string): boolean {
  const match = /(\d+)\.(\d+)/u.exec(actual);
  if (match === null) return false;
  const actualPair = [Number(match[1]), Number(match[2])];
  const minimumPair = minimum.split(".").slice(0, 2).map(Number);
  return actualPair[0] > (minimumPair[0] ?? 0) ||
    (actualPair[0] === minimumPair[0] && actualPair[1] >= (minimumPair[1] ?? 0));
}

class PythonCliView extends FileView {
  private terminal: Terminal | null = null;
  private fitAddon: FitAddon | null = null;
  private session: TerminalSession | null = null;
  private detachSession: (() => void) | null = null;
  private resizeObserver: ResizeObserver | null = null;
  private generation = 0;

  constructor(
    leaf: WorkspaceLeaf,
    private readonly plugin: PythonCliTerminalPlugin,
  ) {
    super(leaf);
  }

  override getViewType(): string {
    return VIEW_TYPE;
  }

  override getDisplayText(): string {
    return this.file?.name ?? "Python CLI";
  }

  override getIcon(): string {
    return "square-terminal";
  }

  override async onLoadFile(file: TFile): Promise<void> {
    await super.onLoadFile(file);
    await this.loadFileContext(file);
  }

  override async onUnloadFile(file: TFile): Promise<void> {
    this.disposeTerminal();
    await super.onUnloadFile(file);
  }

  showConfigurationChanged(): void {
    this.disposeTerminal();
    this.contentEl.empty();
    this.contentEl.createDiv({
      cls: "mud-python-cli-message",
      text: "La configuración cambió. Vuelve a abrir el archivo para reconstruir su contexto.",
    });
  }

  private async loadFileContext(file: TFile): Promise<void> {
    const generation = ++this.generation;
    this.disposeTerminal();
    this.contentEl.empty();
    this.contentEl.addClass("mud-python-cli-view");
    this.contentEl.createDiv({ cls: "mud-python-cli-message", text: "Analizando el CLI sin importar el módulo…" });
    try {
      const absolutePath = this.plugin.absolutePath(file);
      if (!(await this.plugin.ensureEnvironment(absolutePath))) {
        this.contentEl.empty();
        this.contentEl.createDiv({
          cls: "mud-python-cli-message",
          text: "Confirma el entorno del proyecto para analizar y abrir su terminal.",
        });
        return;
      }
      const analysis = await this.plugin.analysis.analyze(absolutePath);
      if (generation !== this.generation) return;
      await this.renderAnalysis(file, analysis);
    } catch (error) {
      if (generation !== this.generation) return;
      const message = error instanceof Error ? error.message : String(error);
      this.contentEl.empty();
      this.contentEl.createDiv({ cls: "mud-python-cli-error", text: `No se pudo analizar el archivo: ${message}` });
    }
  }

  private async renderAnalysis(file: TFile, analysis: CliAnalysis): Promise<void> {
    this.contentEl.empty();
    const header = this.contentEl.createDiv({ cls: "mud-python-cli-header" });
    const title = header.createDiv({ cls: "mud-python-cli-title" });
    title.createEl("strong", { text: file.path });
    const badges = header.createDiv({ cls: "mud-python-cli-badges" });
    badges.createSpan({ text: analysis.kind === "none" ? "sin CLI detectado" : analysis.kind });
    if (analysis.framework !== null) badges.createSpan({ text: analysis.framework });
    badges.createSpan({ text: path.basename(analysis.context.projectRoot) });

    if (analysis.minimumPython !== undefined) {
      const actual = await pythonVersion(this.plugin.settings.pythonExecutable);
      if (!versionAtLeast(actual, analysis.minimumPython)) {
        header.createDiv({
          cls: "mud-python-cli-warning",
          text: `Este CLI requiere Python ${analysis.minimumPython} o posterior; se detectó ${actual}.`,
        });
      }
    }
    if (analysis.diagnostics.length > 0) {
      const details = header.createEl("details", { cls: "mud-python-cli-diagnostics" });
      details.createEl("summary", { text: `${analysis.diagnostics.length} aviso(s) de inspección` });
      for (const diagnostic of analysis.diagnostics) details.createDiv({ text: diagnostic });
    }
    header.createDiv({
      cls: "mud-python-cli-sandbox-warning",
      text: "La inspección --help usa límites de mejor esfuerzo; no es un sandbox de seguridad.",
    });

    const composer = this.contentEl.createDiv({ cls: "mud-python-cli-composer" });
    const input = composer.createEl("input", {
      cls: "mud-python-cli-input",
      attr: {
        type: "text",
        spellcheck: "false",
        "aria-label": "Comando Python",
      },
    });
    input.value = analysis.invocation;
    input.disabled = analysis.kind === "none";
    input.placeholder = analysis.kind === "none" ? "Este módulo no declara un punto de entrada CLI." : "Escribe un comando";
    const runButton = composer.createEl("button", {
      text: "Ejecutar",
      cls: "mod-cta",
      attr: { "aria-label": "Ejecutar comando en la terminal" },
    });
    runButton.disabled = analysis.kind === "none";
    const refreshButton = composer.createEl("button", { text: "Reanalizar" });
    const list = composer.createDiv({ cls: "mud-python-cli-suggestions" });
    list.hide();

    const terminalHost = this.contentEl.createDiv({ cls: "mud-python-cli-terminal" });
    await this.attachTerminal(analysis, terminalHost);

    let current: CompletionResult = { suggestions: [], replaceFrom: input.value.length };
    let selected = 0;
    const renderSuggestions = async (): Promise<void> => {
      current = await complete(input.value, analysis, this.plugin.analysis.customValueProviders);
      if (input.value.trimEnd() === analysis.invocation) {
        const historical = this.plugin
          .historyFor(analysis.context.projectRoot)
          .filter((command) => command.startsWith(`${analysis.invocation} `))
          .map((command) => ({
            value: command.slice(analysis.invocation.length).trimStart(),
            detail: "historial",
          }));
        current.suggestions.unshift(...historical);
      }
      selected = Math.min(selected, Math.max(0, current.suggestions.length - 1));
      list.empty();
      if (current.suggestions.length === 0) {
        list.hide();
        return;
      }
      current.suggestions.slice(0, 30).forEach((suggestion, index) => {
        const row = list.createDiv({
          cls: `mud-python-cli-suggestion${index === selected ? " is-selected" : ""}${suggestion.disabled === true ? " is-disabled" : ""}`,
        });
        row.createSpan({ text: suggestion.label ?? suggestion.value });
        if (suggestion.detail !== undefined) row.createEl("small", { text: suggestion.detail });
        row.addEventListener("mousedown", (event) => {
          event.preventDefault();
          if (suggestion.disabled !== true) acceptSuggestion(suggestion);
        });
      });
      list.show();
    };
    const acceptSuggestion = (suggestion: Suggestion): void => {
      input.value = `${input.value.slice(0, current.replaceFrom)}${suggestion.value} `;
      input.focus();
      list.hide();
      void renderSuggestions();
    };
    const send = (): void => {
      const command = input.value.trim();
      if (command === "" || this.session === null) return;
      this.session.sendCommand(command);
      void this.plugin.recordHistory(analysis.context.projectRoot, command);
      list.hide();
      this.terminal?.focus();
    };

    input.addEventListener("input", () => void renderSuggestions());
    input.addEventListener("keydown", (event) => {
      if (event.ctrlKey && event.code === "Space") {
        event.preventDefault();
        void renderSuggestions();
        return;
      }
      if (event.key === "Escape") {
        list.hide();
        return;
      }
      if (event.key === "ArrowDown" && current.suggestions.length > 0) {
        event.preventDefault();
        selected = (selected + 1) % current.suggestions.length;
        void renderSuggestions();
        return;
      }
      if (event.key === "ArrowUp" && current.suggestions.length > 0) {
        event.preventDefault();
        selected = (selected - 1 + current.suggestions.length) % current.suggestions.length;
        void renderSuggestions();
        return;
      }
      if (event.key === "Tab" && current.suggestions[selected] !== undefined) {
        event.preventDefault();
        const suggestion = current.suggestions[selected];
        if (suggestion?.disabled !== true) acceptSuggestion(suggestion);
        return;
      }
      if (event.key === "Enter") {
        event.preventDefault();
        send();
      }
    });
    input.addEventListener("focus", () => void renderSuggestions());
    runButton.addEventListener("click", send);
    refreshButton.addEventListener("click", () => {
      this.plugin.analysis.clear();
      void this.loadFileContext(file);
    });
  }

  private async attachTerminal(analysis: CliAnalysis, host: HTMLElement): Promise<void> {
    try {
      this.session = await this.plugin.terminals.get(analysis.context.projectRoot);
      this.terminal = new Terminal({
        convertEol: true,
        cursorBlink: true,
        fontFamily: "Cascadia Mono, Consolas, monospace",
        fontSize: 13,
        scrollback: 5_000,
        theme: {
          background: "#111318",
          foreground: "#e6e6e6",
          cursor: "#ffffff",
        },
      });
      this.fitAddon = new FitAddon();
      this.terminal.loadAddon(this.fitAddon);
      this.terminal.open(host);
      this.terminal.onData((data) => this.session?.write(data));
      this.detachSession = this.session.onData((data) => this.terminal?.write(data));
      this.resizeObserver = new ResizeObserver(() => {
        this.fitAddon?.fit();
        if (this.terminal !== null) this.session?.resize(this.terminal.cols, this.terminal.rows);
      });
      this.resizeObserver.observe(host);
      this.fitAddon.fit();
      this.session.resize(this.terminal.cols, this.terminal.rows);
    } catch (error) {
      host.createDiv({
        cls: "mud-python-cli-error",
        text: `No se pudo iniciar la terminal: ${error instanceof Error ? error.message : String(error)}`,
      });
    }
  }

  private disposeTerminal(): void {
    this.resizeObserver?.disconnect();
    this.resizeObserver = null;
    this.detachSession?.();
    this.detachSession = null;
    this.terminal?.dispose();
    this.terminal = null;
    this.fitAddon = null;
    this.session = null;
  }
}

class EnvironmentModal extends Modal {
  private resolved = false;

  constructor(
    app: App,
    private readonly projectRoot: string,
    private readonly settings: PluginSettings,
    private readonly finish: (confirmed: boolean) => void,
  ) {
    super(app);
  }

  override onOpen(): void {
    this.titleEl.setText("Confirmar entorno Python");
    this.contentEl.createEl("p", {
      text: "El análisis estático no importa el módulo. Las sondas --help sí pueden ejecutar código de nivel superior.",
    });
    const values = this.contentEl.createEl("dl", { cls: "mud-python-cli-environment" });
    values.createEl("dt", { text: "Proyecto" });
    values.createEl("dd", { text: this.projectRoot });
    values.createEl("dt", { text: "Python" });
    values.createEl("dd", { text: this.settings.pythonExecutable });
    values.createEl("dt", { text: "Terminal" });
    values.createEl("dd", { text: this.settings.shellExecutable });
    values.createEl("dt", { text: "Puente PTY" });
    values.createEl("dd", { text: this.settings.nodeExecutable });
    const actions = this.contentEl.createDiv({ cls: "modal-button-container" });
    actions.createEl("button", { text: "Cancelar" }).addEventListener("click", () => this.close());
    actions.createEl("button", { text: "Confirmar", cls: "mod-cta" }).addEventListener("click", () => {
      this.resolved = true;
      this.finish(true);
      this.close();
    });
  }

  override onClose(): void {
    if (!this.resolved) this.finish(false);
    this.contentEl.empty();
  }
}

class PythonCliSettingTab extends PluginSettingTab {
  constructor(
    app: App,
    private readonly plugin: PythonCliTerminalPlugin,
  ) {
    super(app, plugin);
  }

  override display(): void {
    this.containerEl.empty();
    new Setting(this.containerEl)
      .setName("Ejecutable de Python")
      .setDesc("Comando o ruta absoluta del intérprete usado para analizar y ejecutar.")
      .addText((text) =>
        text
          .setPlaceholder("python")
          .setValue(this.plugin.settings.pythonExecutable)
          .onChange(async (value) => {
            this.plugin.settings.pythonExecutable = value.trim() || DEFAULT_SETTINGS.pythonExecutable;
            await this.plugin.saveAndRecreate();
          }),
      );
    new Setting(this.containerEl)
      .setName("Ejecutable de Node.js")
      .setDesc("Ejecuta el puente PTY fuera del renderer de Obsidian.")
      .addText((text) =>
        text
          .setPlaceholder("node.exe")
          .setValue(this.plugin.settings.nodeExecutable)
          .onChange(async (value) => {
            this.plugin.settings.nodeExecutable = value.trim() || DEFAULT_SETTINGS.nodeExecutable;
            await this.plugin.saveAndRecreate();
          }),
      );
    new Setting(this.containerEl)
      .setName("PowerShell")
      .setDesc("Se probará primero este ejecutable y después pwsh.exe y powershell.exe.")
      .addText((text) =>
        text
          .setPlaceholder("pwsh.exe")
          .setValue(this.plugin.settings.shellExecutable)
          .onChange(async (value) => {
            this.plugin.settings.shellExecutable = value.trim() || DEFAULT_SETTINGS.shellExecutable;
            await this.plugin.saveAndRecreate();
          }),
      );
  }
}

export default class PythonCliTerminalPlugin extends Plugin {
  override settings: PluginSettings = DEFAULT_SETTINGS;
  analysis!: AnalysisService;
  terminals!: TerminalManager;
  private vaultRoot = "";
  private helperPath = "";
  private pluginRoot = "";

  override async onload(): Promise<void> {
    const adapter = this.app.vault.adapter;
    if (!(adapter instanceof FileSystemAdapter)) {
      throw new Error("Python CLI Terminal necesita una bóveda local de escritorio.");
    }
    this.vaultRoot = adapter.getBasePath();
    this.settings = { ...DEFAULT_SETTINGS, ...(await this.loadData() as Partial<PluginSettings> | null) };
    const pluginDirectory = this.manifest.dir ?? path.join(".obsidian", "plugins", this.manifest.id);
    this.pluginRoot = path.join(this.vaultRoot, pluginDirectory);
    this.helperPath = path.join(this.pluginRoot, "resources", "analyze_cli.py");
    this.createServices();

    this.registerView(VIEW_TYPE, (leaf) => new PythonCliView(leaf, this));
    this.registerExtensions(["py"], VIEW_TYPE);
    this.registerEvent(
      this.app.workspace.on("file-menu", (menu: Menu, file: TAbstractFile) => {
        if (!isPythonFile(file)) return;
        menu.addItem((item) =>
          item
            .setTitle("Abrir CLI Python")
            .setIcon("square-terminal")
            .onClick(() => void this.openFile(file)),
        );
      }),
    );
    this.addCommand({
      id: "open-active-python-cli",
      name: "Abrir CLI Python del archivo activo",
      checkCallback: (checking) => {
        const file = this.app.workspace.getActiveFile();
        if (file === null || !isPythonFile(file)) return false;
        if (!checking) void this.openFile(file);
        return true;
      },
    });
    this.addSettingTab(new PythonCliSettingTab(this.app, this));
  }

  override onunload(): void {
    this.app.workspace.detachLeavesOfType(VIEW_TYPE);
    this.terminals.dispose();
  }

  absolutePath(file: TFile): string {
    return path.join(this.vaultRoot, file.path);
  }

  registerAdapter(adapter: CliAdapter): () => void {
    return this.analysis.registerAdapter(adapter);
  }

  registerValueProvider(provider: ValueProvider): () => void {
    return this.analysis.registerValueProvider(provider);
  }

  historyFor(projectRoot: string): string[] {
    return this.settings.commandHistory[projectRoot] ?? [];
  }

  async recordHistory(projectRoot: string, command: string): Promise<void> {
    const history = this.historyFor(projectRoot).filter((entry) => entry !== command);
    history.unshift(command);
    this.settings.commandHistory[projectRoot] = history.slice(0, 50);
    await this.saveData(this.settings);
  }

  async ensureEnvironment(filePath: string): Promise<boolean> {
    const projectRoot = await findProjectRoot(filePath, this.vaultRoot);
    const signature = [
      this.settings.pythonExecutable,
      this.settings.shellExecutable,
      this.settings.nodeExecutable,
    ].join("\u0000");
    if (this.settings.confirmedProjects[projectRoot] === signature) return true;
    const confirmed = await new Promise<boolean>((resolve) => {
      new EnvironmentModal(this.app, projectRoot, this.settings, resolve).open();
    });
    if (!confirmed) return false;
    this.settings.confirmedProjects[projectRoot] = signature;
    await this.saveData(this.settings);
    return true;
  }

  async saveAndRecreate(): Promise<void> {
    await this.saveData(this.settings);
    this.terminals.dispose();
    this.createServices();
    for (const leaf of this.app.workspace.getLeavesOfType(VIEW_TYPE)) {
      if (leaf.view instanceof PythonCliView) leaf.view.showConfigurationChanged();
    }
  }

  private createServices(): void {
    this.analysis = new AnalysisService(this.vaultRoot, this.helperPath, this.settings.pythonExecutable);
    this.terminals = new TerminalManager(
      this.settings.shellExecutable,
      this.settings.nodeExecutable,
      this.pluginRoot,
    );
  }

  private async openFile(file: TFile): Promise<void> {
    const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE).find(
      (leaf) => leaf.view instanceof PythonCliView && leaf.view.file?.path === file.path,
    );
    if (existing !== undefined) {
      await this.app.workspace.revealLeaf(existing);
      return;
    }
    const leaf = this.app.workspace.getLeaf("tab");
    await leaf.setViewState({
      type: VIEW_TYPE,
      active: true,
      state: { file: file.path },
    });
    await this.app.workspace.revealLeaf(leaf);
  }
}
