// Level 2

datatype Com2 = Print(string)
              | IsAsk(string, string)
              | Assign(string, string)
              | Turn(O2)
              | Forward(O2)
              | Sleep(O2)
              | Seq(Com2, Com2)

datatype O2 = Empty
           | N(int) 
           | V(string) 

type Mem2 = map<string, string> // Loc = string, value string, converteren voor int (onderaan)

trait Env2 
{
    var turtle_exists: bool
    var sigma: Mem2 // memory var-val    
    method Print(output: string) modifies this
    method Ask(question: string) returns (input: string) modifies this
    method Turn(angle: int) modifies this
    method Forward(step: int) modifies this
    method Draw() modifies this
    method Assign(variable: string, value: string) modifies this
    {
        sigma := sigma[variable := value];
    }
    method Sleep(time: int) modifies this
    method SubstText(plaintext: string) returns (valuestext: string) modifies this
    {
        var indexbegin := |plaintext| + 1;
        var indexend := |plaintext| + 1;
        for i := 0 to |plaintext| {
            for j := i to |plaintext| {
                if (plaintext[i..j] in sigma){
                    indexbegin := i; 
                    indexend := j;
                    valuestext := valuestext + sigma[plaintext[i..j]];
                }
            }
            if (i < indexbegin || i > indexend){ // now we can be sure that there is no var at index i
                valuestext := valuestext + [plaintext[i]];
            } 
        }
    }
    method SubstNumber(name: string) returns (number: int) modifies this
    {
        if(name in sigma && |sigma[name]| > 0)
        {
            var temp := strToInt(sigma[name]);
            match(temp){
                case Just(n) => number := n;
                case Nothing => Error("not a number");
            }
        } 
        else {
            Error("not a variable");
        }
    }
    method Error(exception: string) modifies this // turn,forward,sleep used with string instead of int
}

type Config2 = (Com2, Env2)
type Derivation2 = seq<Config2>

method bigstep_level2(c: Com2, e: Env2)
    modifies e
{
    match(c){
        case Print(x) =>
            var temp := e.SubstText(x);
            e.Print(temp);
        case IsAsk(x, y) =>
            var answer := e.Ask(y); // questions cannot yet have variables, so no subst call
            e.Assign(x, answer);
        case Assign(x, y) =>
            e.Assign(x,y);
        case Turn(x) =>
            var num : int;
            match(x) {
                case Empty => num := -90;
                case N(n) => num := n;
                case V(n) => num := e.SubstNumber(n);
            }
            if (e.turtle_exists == false) {
                e.Draw();
                e.turtle_exists := true;
            }
            e.Turn(num);  
        case Forward(x) =>
            var num : int;
            match(x) {
                case Empty => num := 50;
                case N(n) => num := n;
                case V(n) => num := e.SubstNumber(n);
            }
            if (e.turtle_exists == false) {
                e.Draw();
                e.turtle_exists := true;
            }
            e.Forward(num);
        case Sleep(x) =>
            var num : int;
            match(x) {
                case Empty => num := 1;
                case N(n) => num := n;
                case V(n) => num := e.SubstNumber(n);
            }
            e.Sleep(num);
        case Seq(c1, c2) =>
            bigstep_level2(c1, e);
            bigstep_level2(c2, e);
    }
}

// everything from here is for string to int conversion

datatype Maybe<T> = Nothing | Just(T)

predicate method isInt(a: char)
{
  a as int - '0' as int <= 9
}


function method charToInt(a : char): int
requires isInt(a)
{
  a as int - '0' as int
}

method strToInt(a : string) returns(r : Maybe<int>)
  requires |a| > 0
  ensures (forall k :: 0 <= k < |a| ==> isInt(a[k])) ==> exists x :: r == Just(x)
  ensures (exists k :: 0 <= k < |a| && !isInt(a[k])) ==> r == Nothing
{
  if (isInt(a[0])){
    r := Just (charToInt(a[0]));
  }
  else {
    r := Nothing;
  }

  assert !isInt(a[0]) ==> r == Nothing;

  for j := 1 to |a|
    invariant (forall k :: 0 <= k < |a| ==> isInt(a[k])) ==> exists x :: r == Just(x)
    invariant forall k :: 0 <= k < j ==> !isInt(a[k]) ==> r == Nothing
  {
    match r {
      case Nothing => r := Nothing;
      case Just(x) =>
        if (isInt(a[j])){
          r := Just (x * 10 + charToInt(a[j]));
        }
        else {
          r := Nothing;
        }
    }
  }
}
