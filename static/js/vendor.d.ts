// TypeScript typings for libraries we import

// These are provided by skulpt
declare const Sk: {
  pre: string;
  TurtleGraphics?: {
    target?: string;
    width?: number;
    height?: number;
    worldWidth?: number;
    worldHeight?: number;
  };

  builtinFiles?: {
    files: Record<string, string>;
  };

  python3: any;

  configure(options: any): void;

  misceval: {
    asyncToPromise<A>(fn: () => Suspension): Promise<A>;

    Suspension: { }
  },

  importMainWithBody(name: string, dumpJS: boolean, body: string, canSuspend: boolean): Suspension;
}

// These are provided (or used) by Ace, IF Ace is included. The definitions might come from
// somewhere else.
type Module = any;
type RequireFunction = (name: string) => Module;
declare function define(name: string, dependencies: string[], handler: (require: RequireFunction, exports: Module, module: Module) => void): void;

// Apparently Ace also comes with a global require()
declare function require(name: string) => Module;
