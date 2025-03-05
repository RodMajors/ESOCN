declare module 'lua.js' {
  class Lua {
    constructor();
    doString(code: string): Promise<void>;
    global: {
      get(key: string): any;
    };
  }
  export default Lua;
}