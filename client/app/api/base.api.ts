/**
 * バックエンド API を実行するための抽象クラスです.
 */
export abstract class BaseApi<
  ReqBody = undefined,
  QParams extends Record<string, string | number | boolean> | undefined = undefined,
  IRes = unknown,
  Res = unknown,
> {
  static readonly BASE_URL: URL = import.meta.env.DEV
    ? new URL("http://localhost:8000/api/")
    : new URL("/api/", window.location.origin);

  private _path: string;
  protected abstract Response: new (data: IRes) => Res;
  protected abstract resIsIRes(data: unknown): data is IRes;

  constructor(path?: string) {
    this._path = path?.replace(/^\/+/, "") ?? "";
  }

  protected buildUrl(): URL {
    console.log(this._path);
    console.log(BaseApi.BASE_URL);
    return new URL(this._path, BaseApi.BASE_URL);
  }

  /**
   * BASE_URL 以降のパスを設定します.
   * @param {string} path - パス.
   */
  set path(path: string) {
    this._path = path.replace(/^\/+/, "");
  }

  private async get(queryParams?: QParams): Promise<Res | Res[]> {
    const url = this.buildUrl();

    if (queryParams) {
      url.search = new URLSearchParams(Object.entries(queryParams).map(([k, v]) => [k, String(v)])).toString();
    }

    const response = await fetch(url, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
    }

    const json = await response.json();

    if (Array.isArray(json)) {
      if (!json.every((item) => this.resIsIRes(item))) {
        throw new Error("Response array is not valid IRes[]");
      }
      return json.map((item: IRes) => new this.Response(item));
    }
    if (!this.resIsIRes(json)) {
      throw new Error("Response is not valid IRes");
    }
    return new this.Response(json);
  }

  /**
   * GET リクエストを送信し、単一オブジェクトのレスポンスデータを返します.
   *
   * @param {QParams} queryParams - クエリパラメータ.
   * @returns {Promise<Res | Res[]>} - レスポンスデータ.
   * @throws {Error} - レスポンスステータスが 200 以外のときエラーを投げます.
   */
  async getOne(queryParams?: QParams): Promise<Res> {
    const res = await this.get(queryParams);
    if (Array.isArray(res)) {
      throw new Error("Response is array");
    }
    return res;
  }

  /**
   * GET リクエストを送信し、配列のレスポンスデータを返します.
   *
   * @param {QParams} queryParams - クエリパラメータ.
   * @returns {Promise<Res | Res[]>} - レスポンスデータ.
   * @throws {Error} - レスポンスステータスが 200 以外のときエラーを投げます.
   */
  async getArray(queryParams?: QParams): Promise<Res[]> {
    const res = await this.get(queryParams);
    if (!Array.isArray(res)) {
      throw new Error("Response is not array");
    }
    return res;
  }

  /**
   * POST リクエストを送信し、レスポンスステータスを確認します。
   *
   * @param {ReqBody} requestBody - リクエストボディ。
   * @returns {Promise<void>} - レスポンスステータスが 200 のとき void を返します。
   * @throws {Error} - レスポンスステータスが 200 以外のときエラーを投げます。
   */
  async post(requestBody?: ReqBody): Promise<void> {
    const response = await fetch(this.buildUrl(), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody ?? {}),
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
    }
  }
}
