declare module 'fengari' {
    export const lua: any;
    export const lauxlib: any;
    export const lualib: any;
    export const to_luastring: (str: string) => Uint8Array;
}