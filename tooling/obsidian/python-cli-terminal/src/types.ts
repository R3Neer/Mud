export type CliKind = "module" | "script" | "test" | "none";
export type ValueType = "text" | "integer" | "path" | "directory" | "toml";

export interface CliOption {
  names: string[];
  help: string;
  metavar: string | null;
  nargs: string | number | null;
  valueType: ValueType;
  choices: string[];
  takesValue: boolean;
  group: string | null;
}

export interface CliCommand {
  name: string;
  help: string;
  options: CliOption[];
  commands: CliCommand[];
}

export type CliSpec = CliCommand;

export interface StaticAnalysis {
  frameworks: string[];
  hasMainGuard: boolean;
  unittest: boolean;
  spec: CliSpec | null;
  error?: string;
}

export interface HelpProbe {
  arguments: string[];
}

export interface ProjectValueProvider {
  command?: string;
  option: string;
  arguments: string[];
  format: "colon-prefix" | "lines";
  watch?: string[];
}

export interface ProjectCliDefinition {
  path: string;
  module?: string;
  minimumPython?: string;
  disableHelp?: boolean;
  helpProbes?: string[][];
  valueProviders?: ProjectValueProvider[];
}

export interface ProjectCliConfiguration {
  version: number;
  clis: ProjectCliDefinition[];
}

export interface AnalysisContext {
  filePath: string;
  relativePath: string;
  projectRoot: string;
  pythonExecutable: string;
}

export interface CompletionContext {
  analysis: CliAnalysis;
  command: CliCommand | null;
  option: CliOption | null;
  fragment: string;
}

export interface Suggestion {
  value: string;
  label?: string;
  detail?: string;
  disabled?: boolean;
}

export interface CliAdapter {
  id: string;
  detect(context: AnalysisContext): Promise<number>;
  analyzeStatic(context: AnalysisContext): Promise<CliSpec | null>;
  analyzeHelp?(context: AnalysisContext, output: string): Promise<CliSpec | null>;
}

export interface ValueProvider {
  supports(context: CompletionContext): boolean;
  getValues(context: CompletionContext): Promise<Suggestion[]>;
}

export interface CliAnalysis {
  context: AnalysisContext;
  kind: CliKind;
  invocationArgs: string[];
  invocation: string;
  framework: string | null;
  spec: CliSpec | null;
  dynamicValues: Record<string, string[]>;
  diagnostics: string[];
  minimumPython?: string;
}
