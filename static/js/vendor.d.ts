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
