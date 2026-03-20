import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service({ title: "Library Management API" })
@server("http://localhost:5000", "Local development")
namespace Library;

model SuccessResponse<TData> {
  success: true;
  message: string;
  data: TData;
}

model ErrorResponse {
  success: false;
  error: string;
}

model ApiInfo {
  name: string;
  endpoints: string[];
}

model HealthData {
  status: "ok";
}

model Book {
  id: int32;
  title: string;
  author: string;
  year: int32;
  available: boolean;
}

model BookCreateRequest {
  title: string;
  author: string;
  year: int32;
}

model BookUpdateRequest {
  title?: string;
  author?: string;
  year?: int32;
}

model Member {
  id: int32;
  name: string;
  email: string;
}

model BorrowRecord {
  book_id: int32;
  member_id: int32;
  borrowed_at: utcDateTime;
  returned_at: utcDateTime | null;
}

model BorrowRequest {
  book_id: int32;
  member_id: int32;
}

model ReturnRequest {
  book_id: int32;
}

@route("/")
@tag("System")
op apiInfo(): SuccessResponse<ApiInfo>;

@route("/health")
@tag("System")
op healthCheck(): SuccessResponse<HealthData>;

@route("/books")
@tag("Books")
interface BooksApi {
  @get
  listBooks(@query q?: string, @query available?: "true" | "false"): SuccessResponse<Book[]>;

  @post
  createBook(@body body: BookCreateRequest): SuccessResponse<Book> | {
    @statusCode statusCode: 201;
    body: SuccessResponse<Book>;
  } | {
    @statusCode statusCode: 400;
    body: ErrorResponse;
  };
}

@route("/books/{bookId}")
@tag("Books")
interface BookDetailApi {
  @get
  getBook(@path bookId: int32): SuccessResponse<Book> | {
    @statusCode statusCode: 404;
    body: ErrorResponse;
  };

  @put
  updateBook(@path bookId: int32, @body body: BookUpdateRequest): SuccessResponse<Book> | {
    @statusCode statusCode: 400;
    body: ErrorResponse;
  } | {
    @statusCode statusCode: 404;
    body: ErrorResponse;
  };

  @delete
  deleteBook(@path bookId: int32): SuccessResponse<null> | {
    @statusCode statusCode: 404;
    body: ErrorResponse;
  } | {
    @statusCode statusCode: 409;
    body: ErrorResponse;
  };
}

@route("/members")
@tag("Members")
op listMembers(): SuccessResponse<Member[]>;

@route("/borrow")
@tag("Borrow")
op borrowBook(@body body: BorrowRequest): SuccessResponse<BorrowRecord> | {
  @statusCode statusCode: 201;
  body: SuccessResponse<BorrowRecord>;
} | {
  @statusCode statusCode: 400;
  body: ErrorResponse;
} | {
  @statusCode statusCode: 404;
  body: ErrorResponse;
} | {
  @statusCode statusCode: 409;
  body: ErrorResponse;
};

@route("/return")
@tag("Borrow")
op returnBook(@body body: ReturnRequest): SuccessResponse<BorrowRecord> | {
  @statusCode statusCode: 400;
  body: ErrorResponse;
} | {
  @statusCode statusCode: 404;
  body: ErrorResponse;
} | {
  @statusCode statusCode: 409;
  body: ErrorResponse;
};

@route("/borrow-records")
@tag("Borrow")
interface BorrowRecordsApi {
  @get
  listBorrowRecords(): SuccessResponse<BorrowRecord[]>;
}
