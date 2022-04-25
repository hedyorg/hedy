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
  execStart: date;
  execLimit: number;

  builtinFiles?: {
    files: Record<string, string>;
  };

  python3: any;

  configure(options: any): void;

  misceval: {
    asyncToPromise<A>(fn: () => Suspension, handler?: Record<string, () => void>): Promise<A>;

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
declare function require(name: string): Module;

// This is silly bananas to work around a deficiency in the '@types/ace' module:
// it declares all Ace types in a namespace called `AceAjax`, forcing us to write
// `new AceAjax.Range()`, but that namespace doesn't actually exist at runtime (in JavaScript).
// In fact, in the build that we have, the types are globally available (`new Range()`),
// but I can't get TypeScript to mix the AceAjax namespace declarations into the global namespace.
//
// The types also exist on the global variable `ace`, but not according to the type definitions.
// So I'm overriding the type definitions to include both the complete `AceAjax` space (where
// the classes live) as well as the `AceAjax.Ace` interface (where the functions live).
declare var ace: AceAjax & AceAjax.Ace;


// Types for JSConfetti
declare class JSConfetti {
    constructor(options: {
        canvas: HTMLElement
    });

    public addConfetti(): void;
}
