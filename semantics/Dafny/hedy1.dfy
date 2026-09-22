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
datatype P = Empty 
           | N(int)

datatype Maybe<T> = Nothing | Just(elem: T)

trait Env1 
{
    var store: Maybe<string> // remember the answer after ask
    var turtle_exists: bool
    method Print(output: string) modifies this
    method Ask(question: string) returns (input: string) modifies this
    method Error(exception: string) modifies this // echo without ask
    method Turn(angle: int) modifies this
    method Forward(step: int) modifies this
    method Draw() modifies this
}

type Config1 = (Com1, Env1)
type Derivation1 = seq<Config1>

// Used for command turn
function method bigstep_D_level1(d: D): int
{
    match(d){
        case Empty => -90 
        case Left => 90 
        case Right => -90
    }
}

// Used for command forward
function method bigstep_P_level1(p: P): int
{
    match(p){
        case Empty => 50 
        case N(n) => n
    }
}

method bigstep_level1(c: Com1, e: Env1)
    modifies e
{
    match(c){
        case Print(x) =>
            e.Print(x);
        case Ask(x) =>
	          var answer := e.Ask(x);
            e.store := Just(answer);
        case Echo(x) =>
            match(e.store) {
                case Nothing => e.Error("echo without ask");
                case Just(s) => e.Print(x+s);
            }
        case Turn(x) =>
            if (e.turtle_exists == false) {
                e.Draw();
                e.turtle_exists := true;
            }
            e.Turn(bigstep_D_level1(x)); 
        case Forward(x) =>
            if (e.turtle_exists == false) {
                e.Draw();
                e.turtle_exists := true;
            }
            e.Forward(bigstep_P_level1(x));
        case Seq(c1, c2) => {
            bigstep_level1(c1, e);
            bigstep_level1(c2, e);
        }
    }
}