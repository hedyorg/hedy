include "hedy1.dfy"

datatype ActionType
  = PrintT(string)
  | GetT(string)
  | TurnT(int)
  | ForwardT(int)
  | DrawT
  | ExecutionError(string)
  | SampleError

type Sample = seq<string>

class Action {
  var act : ActionType;

  constructor PrintA(output : string)
    ensures act == PrintT(output)
  {
    act := PrintT(output);
  }

  constructor GetA(input : string) {
    act := GetT(input);
  }

  // etc. (one constructor per action

  constructor SampleErrorA() {
    act := SampleError;
  }

}

class SampleEnv1 extends Env1 {
  var samples: Sample;
  var execution : seq<Action>;

  constructor(inputs : seq<string>){
    samples := inputs;
  }

  method Print(output : string)
    modifies this
    ensures |execution| > 0
    ensures execution[0].act == PrintT(output)
  {
    var a := new Action.PrintA(output);
    execution := [a] + execution;
    assert execution[0].act == PrintT(output);
  }

  method Ask(question : string) returns (input : string) modifies this {
    var a := new Action.PrintA(question);
    var b;
    if(|samples| > 0){
      input := samples[0];
      samples := samples[1..];
      b := new Action.GetA(input);
    }
    else {
      b := new Action.SampleErrorA();
    }
    execution := [b, a] + execution;
  }

  method Error(exception: string) modifies this {
  }

  method Turn(angle: int) modifies this {
  }

  method Forward(step: int) modifies this {
  }

  method Draw() modifies this {
  }
}

method Interpret(e1 : SampleEnv1, e2 : Env1)
  modifies e2
  requires e1 != e2 // needed to make sure that we do not interpret e1 in itself
{
  var i := |e1.execution|;
  var j;
  while 0 < i
    decreases i
    invariant 0 <= i
    invariant i <= |e1.execution|
  {
    // for i := |e1.execution| downto 0 {
    j := i - 1;
    i := i - 1;
    match e1.execution[j].act {
      case PrintT(x) => e2.Print(x);
      case _ => return;
    }
  }
}

// Checks whether the last action executed in e was a print with output s
predicate WasPrint(s : string, e : SampleEnv1)
  reads e, e.execution
  requires |e.execution| > 0
{
  e.execution[0].act == PrintT(s)
}

method bigstep_level1_samples(c: Com1, e: SampleEnv1)
  modifies e
  ensures forall x :: c == Print(x) ==> |e.execution| > 0 && WasPrint(x, e)
{
    match(c){
        case Print(x) =>
          e.Print(x);
          assert WasPrint(x, e);
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

twostate predicate SampleDequed(e : SampleEnv1)
  reads e
  requires old(|e.samples|) > 0
{
  old(e.samples[1..]) == e.samples
}


// https://dafny-lang.github.io/dafny/DafnyRef/DafnyRef#sec-old-expression

method PrintCorrect(o : string, e : SampleEnv1)
  modifies e
  ensures |e.execution| > 0
  ensures e.execution[0].act == PrintT(o)

{
  var c := Print(o);
  e.Print(o);
  // bigstep_level1(c, e);
}

/*
method AskCorrect(q : string, e : SampleEnv1)
  modifies e
  requires |e.samples| > 0
{
  var c := Ask(q);
  bigstep_level1(c, e);
  label Executed:
    assert SampleDequed@Executed(e);
}
 */
