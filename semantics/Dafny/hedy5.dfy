// Level 5

datatype Com5 = Print(string)
              | IsAsk(string, string)
              | Assign(string, M)
              | Turn(O5)
              | Forward(O5)
              | Sleep(O5)
              | AddTo(M, L)
              | RemoveFrom(M, L)
              | If(B, Com5)
              | IfElse(B, Com5, Com5)
              | Seq(Com5, Com5)

datatype O5 = Empty | N(int) | V(string) | AtRandom(L) //O5 same as O3, still used from level 3

datatype M = N(int) | V(string) | L(seq<M>) //from level 3 still used

type L = seq<M> // still used from level 3

datatype B = Eq(M, M) // M is M
           | Elem(M, L) // string in L 
            
type Mem5 = map<string, M> // Loc = string

trait Env5
{
    var turtle_exists: bool
    var sigma: Mem5 // memory var-val    
    method Print(output: string) modifies this
    method Ask(question: string) returns (input: M) modifies this
    method Turn(angle: int) modifies this
    method Forward(step: int) modifies this
    method Draw() modifies this
    method Assign(variable: string, value: M) modifies this
    {
        sigma := sigma[variable := value];
    }
    method Sleep(time: int) modifies this
    method SubstText(plaintext: string) returns (valuestext: string) modifies this
    {
        var indexbegin := |plaintext| + 1;
        var indexend := |plaintext| + 1;
        var quotes := false;
        for i := 0 to |plaintext| {
            if (plaintext[i] == '\''){
                quotes := !quotes;
            }
            for j := i to |plaintext| {
                if (plaintext[i..j] in sigma && !quotes){
                    indexbegin := i; 
                    indexend := j;
                    match (sigma[plaintext[i..j]])
                        case N(x) => 
                            Error("Text used without quotes");  
                        case V(x) => 
                            valuestext := valuestext + x;
                        case L(x) => 
                            Error("Cannot print a list"); 
                }
            }
            if ((i < indexbegin || i > indexend) && plaintext[i] != '\''){ // now we can be sure that there is no var at index i
                valuestext := valuestext + [plaintext[i]];
            } 
        }
    }
    method SubstNumber(name: string) returns (number: int) modifies this
    {
        if(name in sigma)
        {
            match (sigma[name]){
                case N(x) => number := x;
                case V(x) => Error("the value of this variable is not a number but a string");
                case L(x) => Error("the value of this variable is not a number but a list");
            }
        } 
        else {
            Error("not a variable");
        }
    }
    method Error(exception: string) modifies this 
    method AddTo(element: M, list: L) modifies this
    method RemoveFrom(element: M, list: L) modifies this
    method Random(list: L) returns (element: M) modifies this
    method Eq(x: M, y: M) returns (cond: bool) modifies this
    {
        match(x, y) {
            case (N(n1), N(n2)) =>
                cond := n1 == n2;
            case (N(n), V(v)) =>
                var temp := SubstNumber(v);
                cond := n == temp;
            case (N(n), L(l)) =>
                Error("Cannot compare list with int");
            case (V(v), N(n)) =>
                var temp := SubstNumber(v);
                cond := n == temp;
            case (V(v1), V(v2)) =>
                var temp1 := SubstText(v1);
                var temp2 := SubstText(v2);
                cond := temp1 == temp2;
            case (V(v), L(l)) =>
                Error("Cannot compare variable or string with list");
            case (L(l), N(n)) =>
                Error("Cannot compare list with int");
            case (L(l), V(v)) =>
                Error("Cannot compare variable or string with list");
            case (L(l1), L(l2)) =>
                cond := l1 == l2;
        }
    }
    method Elem(x: M, y: L) returns (cond: bool) modifies this
    {
        cond := false;
        for i := 0 to |y| {
            if (x == y[i] && cond == false) {cond := true;}
        }
    }
}

type Config5 = (Com5, Env5)
type Derivation5 = seq<Config5>



method bigstep_level5(c: Com5, e: Env5)
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
            e.Assign(x, y);
        case Turn(x) =>
            var num : int;
            match(x) { //x is of type O3
                case Empty => num := -90;
                case N(n) => num := n;
                case V(n) => num := e.SubstNumber(n);
                case AtRandom(l) => {
                    var temp := e.Random(l);
                    match(temp){ // temp is of type M
                        case N(m) => num := m;
                        case V(m) => e.Error("Using variables through a list and at random is not accepted");
                        case L(m) => e.Error("Nesting lists, so using lists of lists is not accepted");
                    }
                }
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
                case AtRandom(l) => {
                    var temp := e.Random(l);
                    match(temp){ // temp is of type M
                        case N(m) => num := m;
                        case V(m) => e.Error("Using variables through a list and at random is not accepted");
                        case L(m) => e.Error("Nesting lists, so using lists of lists is not accepted");
                    }
                }
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
                case AtRandom(l) => {
                    var temp := e.Random(l);
                    match(temp){ // temp is of type M
                        case N(m) => num := m;
                        case V(m) => e.Error("Using variables through a list and at random is not accepted");
                        case L(m) => e.Error("Nesting lists, so using lists of lists is not accepted");
                    }
                }
            }
            e.Sleep(num);
        case AddTo(x, l) => 
            e.AddTo(x,l);
        case RemoveFrom(x, l) =>
            e.RemoveFrom(x,l);
        case If(b, c1) =>
            var condition : bool;
            match(b) {
                case Eq(x, y) => condition := e.Eq(x, y); 
                case Elem(x, y) => condition := e.Elem(x, y);
            }
            if (condition) {bigstep_level5(c1, e);}
        case IfElse(b, c1, c2) =>
            var condition : bool;
            match(b) {
                case Eq(x, y) => condition := e.Eq(x, y);
                case Elem(x, y) => condition := e.Elem(x, y);
            }
            if (condition) {bigstep_level5(c1, e);} else {bigstep_level5(c2, e);}
        case Seq(c1, c2) =>
            bigstep_level5(c1, e);
            bigstep_level5(c2, e);
    } 
}

// everything from here is for conversion of string to int or int to string

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

function method intToChar(a : nat): char
requires a <= 9
{
  a as char + '0' as char
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

method intToStr(a : int) returns(r : string)
{
  r := "";
  var temp1 := a;
  while temp1 > 0
  decreases temp1
  {
    var temp2 := temp1 % 10;
    r := [intToChar(temp2)] + r;
    temp1 := (temp1 - temp2) / 10;
  }
}