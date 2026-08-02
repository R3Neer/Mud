"use strict";

const readline = require("node:readline");

function send(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function fail(error) {
  send({ type: "error", message: error instanceof Error ? error.message : String(error) });
  process.exitCode = 1;
}

const [, , nodePtyPath, shell, cwd, encodedArgs] = process.argv;
if (!nodePtyPath || !shell || !cwd || !encodedArgs) {
  fail(new Error("Faltan argumentos para iniciar el puente PTY."));
} else {
  try {
    const nodePty = require(nodePtyPath);
    const args = JSON.parse(Buffer.from(encodedArgs, "base64url").toString("utf8"));
    const terminal = nodePty.spawn(shell, args, {
      name: "xterm-256color",
      cwd,
      cols: 100,
      rows: 30,
      env: { ...process.env, TERM: "xterm-256color" },
      useConpty: true,
    });
    let closing = false;
    terminal.onData((data) => send({ type: "data", data }));
    terminal.onExit(({ exitCode, signal }) => {
      send({ type: "exit", exitCode, signal });
      process.exitCode = exitCode;
    });
    const input = readline.createInterface({ input: process.stdin, crlfDelay: Infinity });
    input.on("line", (line) => {
      try {
        const message = JSON.parse(line);
        if (message.type === "write" && typeof message.data === "string") {
          terminal.write(message.data);
        } else if (
          message.type === "resize" &&
          Number.isInteger(message.cols) &&
          Number.isInteger(message.rows) &&
          message.cols > 1 &&
          message.rows > 1
        ) {
          terminal.resize(message.cols, message.rows);
        } else if (message.type === "kill") {
          closing = true;
          terminal.kill();
          input.close();
        }
      } catch (error) {
        send({ type: "error", message: `Mensaje inválido: ${String(error)}` });
      }
    });
    input.on("close", () => {
      if (!closing) terminal.kill();
    });
    process.once("SIGTERM", () => terminal.kill());
    process.once("SIGINT", () => terminal.kill());
    send({ type: "ready" });
  } catch (error) {
    fail(error);
  }
}
