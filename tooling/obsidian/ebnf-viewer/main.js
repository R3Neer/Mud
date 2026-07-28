"use strict";

const { Plugin, TextFileView } = require("obsidian");
const { EditorState } = require("@codemirror/state");
const {
  EditorView,
  drawSelection,
  highlightActiveLine,
  highlightActiveLineGutter,
  keymap,
  lineNumbers,
} = require("@codemirror/view");
const {
  bracketMatching,
  StreamLanguage,
  syntaxHighlighting,
} = require("@codemirror/language");
const {
  defaultKeymap,
  history,
  historyKeymap,
  indentWithTab,
} = require("@codemirror/commands");
const { searchKeymap } = require("@codemirror/search");
const { classHighlighter } = require("@lezer/highlight");

const VIEW_TYPE_EBNF = "mud-ebnf-view";

const ebnfLanguage = StreamLanguage.define({
  name: "ebnf",

  startState() {
    return { inComment: false };
  },

  token(stream, state) {
    const atLineStart = stream.sol();

    if (state.inComment) {
      if (stream.skipTo("*)")) {
        stream.match("*)");
        state.inComment = false;
      } else {
        stream.skipToEnd();
      }
      return "comment";
    }

    if (stream.eatSpace()) return null;

    if (stream.match("(*")) {
      if (stream.skipTo("*)")) {
        stream.match("*)");
      } else {
        state.inComment = true;
        stream.skipToEnd();
      }
      return "comment";
    }

    if (stream.peek() === '"') {
      stream.next();
      let escaped = false;
      while (!stream.eol()) {
        const character = stream.next();
        if (character === '"' && !escaped) break;
        escaped = character === "\\" && !escaped;
        if (character !== "\\") escaped = false;
      }
      return "string";
    }

    if (stream.peek() === "?") {
      stream.next();
      while (!stream.eol() && stream.next() !== "?") {
        // Consume an EBNF special sequence.
      }
      return "meta";
    }

    if (
      stream.match(/[A-Za-z][A-Za-z0-9-]*(?=\s*::=)/) ||
      (atLineStart && stream.match(/[A-Za-z][A-Za-z0-9-]*(?=\s*$)/))
    ) {
      return "definition";
    }

    if (stream.match(/::=|:=|->|\.\.|<=>|=>|==|!=|<=|>=|\+=|-=|\*=|\/=|[|,;=]/)) {
      return "operator";
    }

    if (stream.match(/[()[\]{}]/)) return "bracket";
    if (stream.match(/[A-Z][A-Z0-9_]*/)) return "typeName";
    if (stream.match(/[A-Za-z][A-Za-z0-9-]*/)) return "variableName";
    if (stream.match(/[0-9]+/)) return "number";

    stream.next();
    return null;
  },
});

class EbnfView extends TextFileView {
  constructor(leaf) {
    super(leaf);
    this.editorView = null;
    this.editorHost = null;
    this.statusElement = null;
    this.statusTimer = null;
    this.settingData = false;
  }

  getViewType() {
    return VIEW_TYPE_EBNF;
  }

  getDisplayText() {
    return this.file?.name ?? "EBNF";
  }

  getIcon() {
    return "file-code-2";
  }

  async onOpen() {
    this.contentEl.empty();
    this.contentEl.addClass("mud-ebnf-view");

    const toolbar = this.contentEl.createDiv({ cls: "mud-ebnf-toolbar" });
    this.statusElement = toolbar.createSpan({
      cls: "mud-ebnf-status",
      text: "EBNF",
    });
    const saveButton = toolbar.createEl("button", { text: "Guardar" });
    saveButton.type = "button";
    saveButton.addEventListener("click", () => void this.saveNow());

    this.editorHost = this.contentEl.createDiv({ cls: "mud-ebnf-editor" });
    this.editorView = new EditorView({
      state: this.createEditorState(this.data ?? ""),
      parent: this.editorHost,
    });
  }

  async onClose() {
    if (this.statusTimer !== null) window.clearTimeout(this.statusTimer);
    this.editorView?.destroy();
    this.editorView = null;
    this.editorHost = null;
    this.statusElement = null;
  }

  createEditorState(documentText) {
    return EditorState.create({
      doc: documentText,
      extensions: [
        lineNumbers(),
        highlightActiveLineGutter(),
        history(),
        drawSelection(),
        EditorState.allowMultipleSelections.of(true),
        bracketMatching(),
        highlightActiveLine(),
        ebnfLanguage,
        syntaxHighlighting(classHighlighter),
        keymap.of([
          {
            key: "Mod-s",
            preventDefault: true,
            run: () => {
              void this.saveNow();
              return true;
            },
          },
          indentWithTab,
          ...defaultKeymap,
          ...historyKeymap,
          ...searchKeymap,
        ]),
        EditorView.lineWrapping,
        EditorView.updateListener.of((update) => {
          if (!update.docChanged || this.settingData) return;
          this.data = update.state.doc.toString();
          this.requestSave();
          this.showPendingSave();
        }),
      ],
    });
  }

  getViewData() {
    return this.editorView?.state.doc.toString() ?? this.data;
  }

  setViewData(data, clear) {
    this.data = data;
    if (this.editorView === null) return;

    this.settingData = true;
    if (clear) {
      this.editorView.setState(this.createEditorState(data));
    } else {
      this.editorView.dispatch({
        changes: {
          from: 0,
          to: this.editorView.state.doc.length,
          insert: data,
        },
      });
    }
    this.settingData = false;
    this.setStatus("EBNF");
  }

  clear() {
    this.data = "";
    if (this.editorView !== null) {
      this.settingData = true;
      this.editorView.setState(this.createEditorState(""));
      this.settingData = false;
    }
  }

  async saveNow() {
    await this.save();
    this.setStatus("Guardado");
  }

  showPendingSave() {
    this.setStatus("Cambios pendientes…");
    if (this.statusTimer !== null) window.clearTimeout(this.statusTimer);
    this.statusTimer = window.setTimeout(() => {
      this.setStatus("Guardado automáticamente");
      this.statusTimer = null;
    }, 2200);
  }

  setStatus(text) {
    if (this.statusElement !== null) this.statusElement.setText(text);
  }
}

module.exports = class EbnfViewerPlugin extends Plugin {
  async onload() {
    this.registerView(VIEW_TYPE_EBNF, (leaf) => new EbnfView(leaf));
    this.registerExtensions(["ebnf"], VIEW_TYPE_EBNF);
  }
};
