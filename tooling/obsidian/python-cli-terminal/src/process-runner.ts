import { spawn, type ChildProcessByStdio } from "node:child_process";
import type { Readable } from "node:stream";

export interface ProcessResult {
  stdout: string;
  stderr: string;
}

export interface ProcessOptions {
  cwd: string;
  env: NodeJS.ProcessEnv;
  timeoutMs: number;
  maxOutputBytes: number;
}

type LimitedChild = ChildProcessByStdio<null, Readable, Readable>;

async function terminateProcessTree(child: LimitedChild): Promise<void> {
  if (child.exitCode !== null || child.signalCode !== null) return;
  if (process.platform !== "win32" || child.pid === undefined) {
    child.kill("SIGKILL");
    return;
  }
  await new Promise<void>((resolve) => {
    const killer = spawn(
      "taskkill.exe",
      ["/PID", String(child.pid), "/T", "/F"],
      { windowsHide: true, stdio: "ignore" },
    );
    killer.once("error", () => {
      child.kill("SIGKILL");
      resolve();
    });
    killer.once("close", () => resolve());
  });
}

export function runLimitedProcess(
  executable: string,
  arguments_: string[],
  options: ProcessOptions,
): Promise<ProcessResult> {
  return new Promise((resolve, reject) => {
    const child = spawn(executable, arguments_, {
      cwd: options.cwd,
      env: options.env,
      windowsHide: true,
      stdio: ["ignore", "pipe", "pipe"],
    });
    const stdout: Buffer[] = [];
    const stderr: Buffer[] = [];
    let outputSize = 0;
    let settled = false;

    const finish = (error?: Error, result?: ProcessResult): void => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      if (error !== undefined) reject(error);
      else if (result !== undefined) resolve(result);
    };
    const capture = (target: Buffer[]) => (chunk: Buffer): void => {
      outputSize += chunk.length;
      if (outputSize > options.maxOutputBytes) {
        void terminateProcessTree(child).finally(() => {
          finish(new Error(`La salida superó ${options.maxOutputBytes} bytes.`));
        });
        return;
      }
      target.push(chunk);
    };
    child.stdout.on("data", capture(stdout));
    child.stderr.on("data", capture(stderr));
    child.once("error", (error) => finish(error));
    child.once("close", (code, signal) => {
      const result = {
        stdout: Buffer.concat(stdout).toString("utf8"),
        stderr: Buffer.concat(stderr).toString("utf8"),
      };
      if (code === 0) {
        finish(undefined, result);
        return;
      }
      const reason = signal === null ? `código ${String(code)}` : `señal ${signal}`;
      finish(new Error(`El proceso terminó con ${reason}: ${result.stderr.trim()}`));
    });
    const timer = setTimeout(() => {
      void terminateProcessTree(child).finally(() => {
        finish(new Error(`El proceso superó ${options.timeoutMs} ms.`));
      });
    }, options.timeoutMs);
  });
}
