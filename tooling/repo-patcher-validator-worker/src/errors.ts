export class ServiceError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly status = 400,
    public readonly retryable = false,
  ) {
    super(message);
    this.name = "ServiceError";
  }
}

export function errorResponse(error: unknown): Response {
  if (error instanceof ServiceError) {
    return Response.json(
      { code: error.code, message: error.message, retryable: error.retryable },
      {
        status: error.status,
        headers: error.retryable ? { "Retry-After": "1" } : undefined,
      },
    );
  }
  console.error("Unhandled validator Worker error", error);
  return Response.json({ code: "internal_error", retryable: false }, { status: 500 });
}
