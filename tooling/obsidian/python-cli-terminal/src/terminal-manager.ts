import { execFile, spawn, type ChildProcessByStdio } from "node:child_process";
import path from "node:path";
import type { Readable, Writable } from "node:stream";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

type DataListener = (data: string) => void;
type BridgeChild = ChildProcessByStdio<Writable, Readable, Readable>;

interface BridgeMessage {
  type: "ready" | "data" | "error" | "exit";
  data?: string;
  message?: string;
  exitCode?: number;
}

function encodeArguments(arguments_: string[]): string {
  return Buffer.from(JSON.stringify(arguments_), "utf8").toString("base64url");
}

export async function detectPowerShell(preferred: string): Promise<string[]> {
  const candidates = [preferred, "pwsh.exe", "powershell.exe"].filter(
    (value, index, values) => value.trim() !== "" && values.indexOf(value) === index,
  );
  for (const candidate of candidates) {
    try {
      await execFileAsync("where.exe", [candidate], { windowsHide: true, timeout: 2_000 });
      return [candidate, "-NoLogo"];
    } catch {
      // Try the next shell.
    }
  }
  return ["powershell.exe", "-NoLogo"];
}

export class TerminalSession {
  private readonly listeners = new Set<DataListener>();
  private disposed = false;
  private stdoutBuffer = "";

  private constructor(
    readonly projectRoot: string,
    private readonly child: BridgeChild,
  ) {
    child.stdout.setEncoding("utf8");
    child.stdout.on("data", (chunk: string | Buffer) => this.capture(String(chunk)));
    child.stderr.setEncoding("utf8");
    child.stderr.on("data", (chunk: string | Buffer) => {
      this.emit(`\r\n[PTY] ${String(chunk).trim()}\r\n`);
    });
  }

  static create(
    projectRoot: string,
    nodeExecutable: string,
    bridgePath: string,
    nodePtyPath: string,
    shell: string,
    shellArguments: string[],
  ): Promise<TerminalSession> {
    return new Promise((resolve, reject) => {
      const child = spawn(
        nodeExecutable,
        [bridgePath, nodePtyPath, shell, projectRoot, encodeArguments(shellArguments)],
        {
          cwd: projectRoot,
          env: process.env,
          windowsHide: true,
          stdio: ["pipe", "pipe", "pipe"],
        },
      );
      const session = new TerminalSession(projectRoot, child);
      let settled = false;
      const timer = setTimeout(() => {
        if (settled) return;
        settled = true;
        session.dispose();
        reject(new Error("El puente PTY no respondió en 5000 ms."));
      }, 5_000);
      const ready = (message: BridgeMessage): void => {
        if (settled) return;
        if (message.type === "ready") {
          settled = true;
          clearTimeout(timer);
          session.bridgeListeners.delete(ready);
          resolve(session);
        } else if (message.type === "error") {
          settled = true;
          clearTimeout(timer);
          session.bridgeListeners.delete(ready);
          session.dispose();
          reject(new Error(message.message ?? "El puente PTY falló."));
        }
      };
      session.bridgeListeners.add(ready);
      child.once("error", (error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        session.bridgeListeners.delete(ready);
        reject(error);
      });
      child.once("exit", (code) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        session.bridgeListeners.delete(ready);
        reject(new Error(`El puente PTY terminó durante el arranque con código ${String(code)}.`));
      });
    });
  }

  private readonly bridgeListeners = new Set<(message: BridgeMessage) => void>();

  onData(listener: DataListener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  write(data: string): void {
    this.send({ type: "write", data });
  }

  sendCommand(command: string): void {
    this.write(`${command}\r`);
  }

  resize(cols: number, rows: number): void {
    if (cols > 1 && rows > 1) this.send({ type: "resize", cols, rows });
  }

  dispose(): void {
    if (this.disposed) return;
    this.disposed = true;
    this.send({ type: "kill" });
    this.listeners.clear();
    this.bridgeListeners.clear();
    const child = this.child;
    setTimeout(() => {
      if (child.exitCode === null && child.signalCode === null) child.kill();
    }, 1_000);
  }

  private send(message: object): void {
    if (this.disposed && !("type" in message && message.type === "kill")) return;
    if (this.child.stdin.destroyed) return;
    this.child.stdin.write(`${JSON.stringify(message)}\n`);
  }

  private capture(chunk: string): void {
    this.stdoutBuffer += chunk;
    let newline = this.stdoutBuffer.indexOf("\n");
    while (newline >= 0) {
      const line = this.stdoutBuffer.slice(0, newline).trim();
      this.stdoutBuffer = this.stdoutBuffer.slice(newline + 1);
      if (line !== "") {
        try {
          const message = JSON.parse(line) as BridgeMessage;
          for (const listener of this.bridgeListeners) listener(message);
          if (message.type === "data" && message.data !== undefined) this.emit(message.data);
          if (message.type === "error") this.emit(`\r\n[PTY] ${message.message ?? "Error desconocido"}\r\n`);
        } catch (error) {
          this.emit(`\r\n[PTY] Respuesta inválida: ${String(error)}\r\n`);
        }
      }
      newline = this.stdoutBuffer.indexOf("\n");
    }
  }

  private emit(data: string): void {
    for (const listener of this.listeners) listener(data);
  }
}

export class TerminalManager {
  private readonly sessions = new Map<string, TerminalSession>();

  constructor(
    private readonly shellExecutable: string,
    private readonly nodeExecutable: string,
    private readonly pluginRoot: string,
  ) {}

  async get(projectRoot: string): Promise<TerminalSession> {
    const existing = this.sessions.get(projectRoot);
    if (existing !== undefined) return existing;
    const [shell, ...args] = await detectPowerShell(this.shellExecutable);
    if (shell === undefined) throw new Error("No se encontró PowerShell.");
    const session = await TerminalSession.create(
      projectRoot,
      this.nodeExecutable,
      path.join(this.pluginRoot, "resources", "pty_bridge.cjs"),
      path.join(this.pluginRoot, "node_modules", "node-pty"),
      shell,
      args,
    );
    this.sessions.set(projectRoot, session);
    return session;
  }

  dispose(): void {
    for (const session of this.sessions.values()) session.dispose();
    this.sessions.clear();
  }
}
