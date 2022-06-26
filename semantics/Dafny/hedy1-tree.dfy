include "hedy1.dfy"

// https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/krml250.pdf
//  https://github.com/dafny-lang/dafny/blob/master/Test/dafny4/NipkowKlein-chapter7.dfy

  // Record type with one field for the store and one to indicate whether the turtle
// has already been drawn.
datatype State = State(store : Maybe<string>, drawn : bool)

// Type that represents interactions with the environment as tree
datatype Prog<A>
  = Return (pure : A)
  | PrintP(output : string, Prog<A>)
  | AskP(question : string, input : string -> Prog<A>)
  | TurnP(angle : int, Prog<A>)
  | ForwardP(step : int, Prog<A>)
  | DrawP(Prog<A>)
  | Error(exception : string)


// We give the big-step semantics as two mutually recursively defined inductive
// relations. big_step_seq is used to sequentially compose the semantics of two
// commands.

least predicate big_step_seq(c : Com1, p : Prog<State>, q : Prog<State>) {
  match p {
    case Return(s) => big_step(c, s, q)
    case PrintP(o, p') => exists q' :: q == PrintP(o, q') && big_step_seq(c, p', q')
    case AskP(o, f) => exists g :: q == AskP(o, g) &&  forall i :: big_step_seq(c, f(i), g(i))
    case TurnP(a, p') => false
    case ForwardP(x, p') => false
    case DrawP(p') => exists q' :: q == DrawP(q') && big_step_seq(c, p', q')
    case Error(e) => q == Error(e)
  }
}


least predicate big_step(c : Com1, s : State, p : Prog<State>) {
  match c {
    case Print(o) => p == PrintP(o, Return(s))
    case Ask(o) =>
      p == AskP(o, i => Return(s.(store := Just(i))))
    case Echo(o) =>
      match s.store {
        case Nothing => p == Error("echo without ask")
        case Just(x) => p == PrintP(o + x, Return(s))
      }
    case Turn(x) =>
      p == TurnP(bigstep_D_level1(x), Return(s))
    case Forward(x) => p == ForwardP(bigstep_P_level1(x), Return(s))
    case Seq(c1, c2) =>
      exists p1 :: big_step(c1, s, p1) && big_step_seq(c2, p1, p)
  }
}

lemma PrintCorrect(o : string, s : State)
  ensures forall p :: big_step(Print(o), s, p) ==> p == PrintP(o, Return(s));
{ }

predicate readStore(p : Prog<State>, v : string) {
  match p {
    case Return(s) =>
      match s.store {
        case Nothing => false
        case Just (x) => x == v
      }
     case _ => false
  }
}

lemma AskCorrect(o : string, s : State, p : Prog<State>)
  requires big_step(Ask(o), s, p)
  ensures exists f :: p == AskP(o, f) && forall i :: readStore(f(i), i)
{ }

lemma big_step_seq_return(c : Com1, s : State)
  ensures forall p :: big_step_seq(c, Return(s), p) ==> big_step(c, s, p)
{ }

lemma PrintSeq(c : Com1, o : string, s : State, p : Prog<State>)
  requires big_step(Seq(Print(o), c), s, p)
  ensures exists q :: p == PrintP(o, q) && big_step(c, s, q)
{
  big_step_seq_return(c, s);
}

lemma SimpleSeq(o : string, s : State, p : Prog<State>)
  requires big_step(Seq(Print(o), Ask(o)), s, p)
{
  PrintSeq(Ask(o), o, s, p);
  assert exists q :: p == PrintP(o, q) && big_step(Ask(o), s, q);
}

// lemma big_step_deterministic_aux(k: ORDINAL, k': ORDINAL, c: Com1, s: State, p: Prog<State>, p': Prog<State>)
//   requires big_step#[k](c, s, p) && big_step#[k'](c, s, p')
//   ensures p == p'
// {}


least predicate wfTree<T> (p : Prog<T>){
  match p {
    case Return(b) => true
    case PrintP(_, p') => wfTree(p')
    case AskP(_, g) => forall x :: wfTree(g(x))
    case TurnP(_, p') => wfTree(p')
    case ForwardP(_, p') => wfTree(p')
    case DrawP(p') => wfTree(p')
    case Error(_) => true
  }
}

// // Not executable because it tests for limit ordinals
// method run_aux(ghost k :ORDINAL, p : Prog<State>, e : Env1)
//   requires wfTree#[k](p)
//   decreases k
// {
//   if(k.IsLimit) {
//     ghost var m :| m < k && wfTree#[m](p);
//     run_aux(m, p, e);
//   }
//   else {
//     match p {
//       case Return(s) => return;
//       case PrintP(o, q) =>
//         e.Print(o);
//         run_aux(k-1, q, e);
//       case AskP(o, f) =>
//         var i := e.Ask(o);
//         run_aux(k-1, f(i), e);
//       case TurnP(a, p') =>
//         e.Turn(a);
//         run_aux(k-1, p', e);
//       case ForwardP(x, p') =>
//         e.Forward(x);
//         run_aux(k-1, p', e);
//       case DrawP(p') =>
//         e.Draw();
//         run_aux(k-1, p', e);
//       case Error(x) =>
//         e.Error(x);
//     }
//   }
// }

// method runP(p : Prog<State>, e : Env1)
//   requires wfTree(p)
// {
//   ghost var k :| wfTree#[k](p);
//   run_aux(k, p, e);
// }


// Unsafe declaration but Dafny does not understand that this method
// is terminating because of the higher-order argument of Get.
method {: verify false} run(p : Prog<State>, e : Env1)
  modifies e
{
  match p {
    case Return(s) => return;
    case PrintP(o, q) =>
      e.Print(o);
      run(q, e);
    case AskP(o, f) =>
      var i := e.Ask(o);
      run(f(i), e);
    case TurnP(a, p') =>
      e.Turn(a);
      run(p', e);
    case ForwardP(x, p') =>
      e.Forward(x);
      run(p', e);
    case DrawP(p') =>
      e.Draw();
      run(p', e);
    case Error(x) =>
      e.Error(x);
  }
}
