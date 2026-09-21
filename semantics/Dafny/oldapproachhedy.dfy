// Level 1

datatype Com1 = Print(string)
              | Ask(string)
              | Echo(string)
              | Turn(D)
              | Forward(P)
              | Seq(Com1, Com1) 

// Used for command turn
datatype D = Empty
           | Left
           | Right

// Used for command forward
datatype P = Empty //empty meteen 50?
           | N(int)


//type Env = map<Var, Val>
class Env1 
{
    var outs: string // string voor outputs
    var ins: string // string met laatst ingevoerde input
    var turtle: string // TODO structuur voor turtle (commands/grid/bitmap...?) boolean turtle exists?
}

type Config1 = (Com1, Env1)
type Derivation1 = seq<Config1>

// Used for command turn
function bigstep_D_level1(d: D): int
{
    match(d){
        case Empty => -90 
        case "left" => 90 // does this work?
        case "right" => -90
    }
}

// Used for command forward
function bigstep_P_level1(p: P): int
{
    match(p){
        case Empty => 50 
        case N(n) => n
    }
}

//k is to prevent non-termination
predicate bigstep_level1(c: Com1, e: Env1, e': Env1, k: nat)
    decreases c,k
{
    match(c){
        case Print(x) =>
            k == 1 && e[outs := e.outs + "\n" + x] == e' // klopt syntax?
        case Ask(x) =>
            k == 1 && e == e' // TODO?? replace ins with what? how to get input? how add&remove question?
        case Echo(x) =>
            k == 1 && e[outs := e.outs + "\n" + x + e.ins] == e' // klopt syntax?
        case Turn(d) =>
            k == 1 && e[turtle := e.turtle + "\n" + "turn " + bigstep_D_level1(d)] == e' // TODO klopt syntax? zo houden we de commando's bij om de turtle animatie te weten, geen bitmap of zo.
        case Forward(p) =>
            k == 1 && e[turtle := e.turtle + "\n" + "forward " + bigstep_P_level1(p)] == e' // TODO??
        case Seq(c1, c2) =>
            exists k': nat, e'': Env1 :: 
                0 < k' < k &&
                bigstep_level1(c1, e, e'', k') &&
                bigstep_level1(c2, e'', e', k-k')                
                //e'' and e' are other way around in my rule on paper.
    }
}


// Level 2

datatype Com2 = Print(string)
              | IsAsk(string, string)
              | Assign(string, string)
              | Turn(O2)
              | Forward(O2)
              | Sleep(O2)
              | Seq(Com2, Com2)

datatype O2 = Empty
           | M

datatype M = N(int)
           | V(string)

// Used for commands turn, forward, sleep
function bigstep_O2(c: Com2, o: O2, e: Env2): int
{
    match(o){
        case Empty => 
            match(c){
                case Turn(o) => -90
                case Forward(o) => 50
                case Sleep(o) => 1
            }
        case N(n) => n
        case V(x) => if x in e then e[x] else 0 // else moet een exception geven?
    }
}

class Env2 
{
    var outs: string // string voor outputs
    //type sigma = map<string, string> // memory, Loc > A* // of var sigma : array<string> ?
    var turtle: string // TODO structuur voor turtle (commands/grid/bitmap...?) boolean turtle exists
}

type Config2 = (Com2, Env2)
type Derivation2 = seq<Config2>

//k is to prevent non-termination
predicate bigstep_level2(c: Com2, e: Env2, e': Env2, k: nat)
    decreases c,k
{
    match(c){
        case Print(x) =>
            k == 1 && e[outs := e.outs + "\n" + x] == e' // add substitution of vars
        case IsAsk(x, y) =>
            k == 1 && e == e' // TODO?? replace ins with what? how add&remove question?
        case Assign(x, y) =>
            k == 1 && e[sigma(x) := y] == e'
        case Turn(x) =>
            k == 1 && e[turtle := e.turtle + "\n" + "turn " + bigstep_O2(d)] == e' // TODO klopt syntax? zo houden we de commando's bij om de turtle animatie te weten, geen bitmap of zo.
        case Forward(x) =>
            k == 1 && e[turtle := e.turtle + "\n" + "forward " + bigstep_O2(p)] == e'
        case Sleep(x) =>
            k == 1 && e == e' // TODO?? dit is skip, niet helemaal zelfde als sleep.
        case Seq(c1, c2) =>
            exists k': nat, e'': Env1 :: 
                0 < k' < k &&
                bigstep_level2(c1, e, e'', k') &&
                bigstep_level2(c2, e'', e', k-k') 
                //e'' and e' are other way around in my rule on paper.
    }
}


// Level 3

datatype Com3 = Print(string)
              | IsAsk(string, string)
              | Assign(string, string)
              | Turn(O3)
              | Forward(O3)
              | Sleep(O3)
              | AddTo(string, L)
              | RemoveFrom(string, L)
              | Seq(Com3, Com3)

datatype O3 = Empty
           | U

datatype U = N(int)
           | V(string)
           | AtRandom(L)

// datatype M = N(int) | V(string) from level 2 still used

//datatype L = M, M | L, M doesnt work
type L = array<M>


// Used for commands turn, forward, sleep
function bigstep_O3(c: Com3, o: O3, e: Env3): int
{
    match(o){
        case Empty => 
            match(c){
                case Turn(o) => -90
                case Forward(o) => 50
                case Sleep(o) => 1
            }
        case N(n) => n
        case V(x) => if x in e then e[x] else 0 // else moet een exception geven?
        case AtRandom(l) => l[0] //TODO?? now chooses first one
    }
}

//type T = string | int

class Env3 
{
    var outs: string // string voor outputs
    // var sigma : array<T> // TODO memory, Loc > disjoint union of A*, Z, ListT
    var turtle: string // TODO structuur voor turtle (commands/grid/bitmap...?) boolean turtle exists
}

type Config3 = (Com3, Env3)
type Derivation3 = seq<Config3>

//k is to prevent non-termination
predicate bigstep_level3(c: Com3, e: Env3, e': Env3, k: nat)
    decreases c,k
{
    match(c){
        case Print(x) =>
            k == 1 && e[outs := e.outs + "\n" + x] == e' // add substitution of vars
        case IsAsk(x, y) =>
            k == 1 && e == e' // TODO?? replace ins with what? how add&remove question?
        case Assign(x, y) =>
            k == 1 && e[sigma(x) := y] == e'
        case Turn(x) =>
            k == 1 && e[turtle := e.turtle + "\n" + "turn " + bigstep_O3(c, x)] == e' // TODO klopt syntax? zo houden we de commando's bij om de turtle animatie te weten, geen bitmap of zo.
        case Forward(x) =>
            k == 1 && e[turtle := e.turtle + "\n" + "forward " + bigstep_O3(c, x)] == e'
        case Sleep(x) =>
            k == 1 && e == e' // TODO?? dit is skip, niet helemaal zelfde als sleep.
        //case AddTo(x, l) =>
        //    k == 1 && e[sigma...] == e' //TODO?
        //case RemoveFrom(x, l) =>
        //    k == 1 && e[sigma...] == e' //TODO?
        case Seq(c1, c2) =>
            exists k': nat, e'': Env1 :: 
                0 < k' < k &&
                bigstep_level3(c1, e, e'', k') &&
                bigstep_level3(c2, e'', e', k-k') 
                //e'' and e' are other way around in my rule on paper.
    }
}


// Level 4 is the same as level 3

// Level 5

datatype Com5 = Print(string)
              | IsAsk(string, string)
              | Assign(string, string)
              | Turn(O3)
              | Forward(O3)
              | Sleep(O3)
              | AddTo(string, L)
              | RemoveFrom(string, L)
              | If(B, Com5)
              | IfElse(B, Com5, Com5)
              | Seq(Com5, Com5)

// datatype O3 = Empty | U still used from level 3

// datatype U = N(int) | V(string) | AtRandom(L) still used from level 3

// datatype M = N(int) | V(string) from level 2 still used

// datatype L = M, M | L, M still used from level 3

datatype B = Elem(string, L) // string in L 
           | Eq(M, M) // M is M

// function bigstep_O3 still used

function bigstep_if_condition(b: B, e: Env5): bool
{
    match(b){
        //case Elem(x, y) => //TODO??
        case Eq(x, y) => x == y // TODO variabelen en zo fixen
    }
}

class Env5 
{
    var outs: string // string voor outputs
    //function sigma(string): string // TODO memory, Loc > disjoint union of A*, Z, ListT, BOOLEAN (bool is nieuw)
    var turtle: string // TODO structuur voor turtle (commands/grid/bitmap...?) boolean turtle exists
}

type Config5 = (Com5, Env5)
type Derivation5 = seq<Config5>

//k is to prevent non-termination
predicate bigstep_level5(c: Com5, e: Env5, e': Env5, k: nat)
    decreases c,k
{
    match(c){
        case Print(x) =>
            k == 1 && e[outs := e.outs + "\n" + x] == e' // add substitution of vars
        case IsAsk(x, y) =>
            k == 1 && e == e' // TODO?? replace ins with what? how add&remove question?
        case Assign(x, y) =>
            k == 1 && e[sigma(x) := y] == e'
        case Turn(x) =>
            k == 1 && e[turtle := e.turtle + "\n" + "turn " + bigstep_O3(c, x)] == e' // TODO klopt syntax? zo houden we de commando's bij om de turtle animatie te weten, geen bitmap of zo.
        case Forward(x) =>
            k == 1 && e[turtle := e.turtle + "\n" + "forward " + bigstep_O3(c, x)] == e'
        case Sleep(x) =>
            k == 1 && e == e' // TODO?? dit is skip, niet helemaal zelfde als sleep.
        //case AddTo(x, l) =>
        //    k == 1 && e[sigma...] == e' //TODO?
        //case RemoveFrom(x, l) =>
        //    k == 1 && e[sigma...] == e' //TODO?
        case If(b, c) =>
            if(bigstep_if_condition(b, e)) then bigstep_level5(c, e, e', k) else k == 1 && e == e'
        case IfElse(b, c1, c2) =>
            if(bigstep_if_condition(b, e)) then bigstep_level5(c1, e, e', k) else bigstep_level5(c2, e, e', k)
        case Seq(c1, c2) =>
            exists k': nat, e'': Env1 :: 
                0 < k' < k &&
                bigstep_level3(c1, e, e'', k') &&
                bigstep_level3(c2, e'', e', k-k') 
                //e'' and e' are other way around in my rule on paper.
    }
}