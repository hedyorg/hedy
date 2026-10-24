// Dafny program hedy5.dfy compiled into C#
// To recompile, you will need the libraries
//     System.Runtime.Numerics.dll System.Collections.Immutable.dll
// but the 'dotnet' tool in net6.0 should pick those up automatically.
// Optionally, you may want to include compiler switches like
//     /debug /nowarn:162,164,168,183,219,436,1717,1718

using System;
using System.Numerics;
[assembly: DafnyAssembly.DafnySourceAttribute(@"// Dafny 3.5.0.40314
// Command Line Options: /spillTargetCode:2 .\hedyindafny\hedy5.dfy
// hedy5.dfy

datatype Com5 = Print(string) | IsAsk(string, string) | Assign(string, M) | Turn(O5) | Forward(O5) | Sleep(O5) | AddTo(M, L) | RemoveFrom(M, L) | If(B, Com5) | IfElse(B, Com5, Com5) | Seq(Com5, Com5)

datatype O5 = Empty | N(int) | V(string) | AtRandom(L)

datatype M = N(int) | V(string) | L(seq<M>)

type L = seq<M>

datatype B = Eq(M, M) | Elem(M, L)

type Mem5 = map<string, M>

trait Env5 {
  var turtle_exists: bool
  var sigma: Mem5

  method Print(output: string)
    modifies this
    decreases output

  method Ask(question: string) returns (input: M)
    modifies this
    decreases question

  method Turn(angle: int)
    modifies this
    decreases angle

  method Forward(step: int)
    modifies this
    decreases step

  method Draw()
    modifies this

  method Assign(variable: string, value: M)
    modifies this
    decreases variable, value
  {
    sigma := sigma[variable := value];
  }

  method Sleep(time: int)
    modifies this
    decreases time

  method SubstText(plaintext: string) returns (valuestext: string)
    modifies this
    decreases plaintext
  {
    var indexbegin := |plaintext| + 1;
    var indexend := |plaintext| + 1;
    var quotes := false;
    for i: int := 0 to |plaintext| {
      if plaintext[i] == '\'' {
        quotes := !quotes;
      }
      for j: int := i to |plaintext| {
        if plaintext[i .. j] in sigma && !quotes {
          indexbegin := i;
          indexend := j;
          match sigma[plaintext[i .. j]]
          case {:split false} N(x) =>
            Error(""Text used without quotes"");
          case {:split false} V(x) =>
            valuestext := valuestext + x;
          case {:split false} L(x) =>
            Error(""Cannot print a list"");
        }
      }
      if (i < indexbegin || i > indexend) && plaintext[i] != '\'' {
        valuestext := valuestext + [plaintext[i]];
      }
    }
  }

  method SubstNumber(name: string) returns (number: int)
    modifies this
    decreases name
  {
    if name in sigma {
      match sigma[name] {
        case {:split false} N(x) =>
          number := x;
        case {:split false} V(x) =>
          Error(""the value of this variable is not a number but a string"");
        case {:split false} L(x) =>
          Error(""the value of this variable is not a number but a list"");
      }
    } else {
      Error(""not a variable"");
    }
  }

  method Error(exception: string)
    modifies this
    decreases exception

  method AddTo(element: M, list: L)
    modifies this
    decreases element, list

  method RemoveFrom(element: M, list: L)
    modifies this
    decreases element, list

  method Random(list: L) returns (element: M)
    modifies this
    decreases list

  method Eq(x: M, y: M) returns (cond: bool)
    modifies this
    decreases x, y
  {
    match (x, y) {
      case {:split false} (N(n1), N(n2)) =>
        cond := n1 == n2;
      case {:split false} (N(n), V(v)) =>
        var temp := SubstNumber(v);
        cond := n == temp;
      case {:split false} (N(n), L(l)) =>
        Error(""Cannot compare list with int"");
      case {:split false} (V(v), N(n)) =>
        var temp := SubstNumber(v);
        cond := n == temp;
      case {:split false} (V(v1), V(v2)) =>
        var temp1 := SubstText(v1);
        var temp2 := SubstText(v2);
        cond := temp1 == temp2;
      case {:split false} (V(v), L(l)) =>
        Error(""Cannot compare variable or string with list"");
      case {:split false} (L(l), N(n)) =>
        Error(""Cannot compare list with int"");
      case {:split false} (L(l), V(v)) =>
        Error(""Cannot compare variable or string with list"");
      case {:split false} (L(l1), L(l2)) =>
        cond := l1 == l2;
    }
  }

  method Elem(x: M, y: L) returns (cond: bool)
    modifies this
    decreases x, y
  {
    cond := false;
    for i: int := 0 to |y| {
      if x == y[i] && cond == false {
        cond := true;
      }
    }
  }
}

type Config5 = (Com5, Env5)

type Derivation5 = seq<Config5>

datatype Maybe<T> = Nothing | Just(T)

method bigstep_level5(c: Com5, e: Env5)
  modifies e
  decreases c, e
{
  match c {
    case {:split false} Print(x) =>
      var temp := e.SubstText(x);
      e.Print(temp);
    case {:split false} IsAsk(x, y) =>
      var answer := e.Ask(y);
      e.Assign(x, answer);
    case {:split false} Assign(x, y) =>
      e.Assign(x, y);
    case {:split false} Turn(x) =>
      var num: int;
      match x {
        case {:split false} Empty =>
          num := -90;
        case {:split false} N(n) =>
          num := n;
        case {:split false} V(n) =>
          num := e.SubstNumber(n);
        case {:split false} AtRandom(l) =>
          {
            var temp := e.Random(l);
            match temp {
              case {:split false} N(m) =>
                num := m;
              case {:split false} V(m) =>
                e.Error(""Using variables through a list and at random is not accepted"");
              case {:split false} L(m) =>
                e.Error(""Nesting lists, so using lists of lists is not accepted"");
            }
          }
      }
      if e.turtle_exists == false {
        e.Draw();
        e.turtle_exists := true;
      }
      e.Turn(num);
    case {:split false} Forward(x) =>
      var num: int;
      match x {
        case {:split false} Empty =>
          num := 50;
        case {:split false} N(n) =>
          num := n;
        case {:split false} V(n) =>
          num := e.SubstNumber(n);
        case {:split false} AtRandom(l) =>
          {
            var temp := e.Random(l);
            match temp {
              case {:split false} N(m) =>
                num := m;
              case {:split false} V(m) =>
                e.Error(""Using variables through a list and at random is not accepted"");
              case {:split false} L(m) =>
                e.Error(""Nesting lists, so using lists of lists is not accepted"");
            }
          }
      }
      if e.turtle_exists == false {
        e.Draw();
        e.turtle_exists := true;
      }
      e.Forward(num);
    case {:split false} Sleep(x) =>
      var num: int;
      match x {
        case {:split false} Empty =>
          num := 1;
        case {:split false} N(n) =>
          num := n;
        case {:split false} V(n) =>
          num := e.SubstNumber(n);
        case {:split false} AtRandom(l) =>
          {
            var temp := e.Random(l);
            match temp {
              case {:split false} N(m) =>
                num := m;
              case {:split false} V(m) =>
                e.Error(""Using variables through a list and at random is not accepted"");
              case {:split false} L(m) =>
                e.Error(""Nesting lists, so using lists of lists is not accepted"");
            }
          }
      }
      e.Sleep(num);
    case {:split false} AddTo(x, l) =>
      e.AddTo(x, l);
    case {:split false} RemoveFrom(x, l) =>
      e.RemoveFrom(x, l);
    case {:split false} If(b, c1) =>
      var condition: bool;
      match b {
        case {:split false} Eq(x, y) =>
          condition := e.Eq(x, y);
        case {:split false} Elem(x, y) =>
          condition := e.Elem(x, y);
      }
      if condition {
        bigstep_level5(c1, e);
      }
    case {:split false} IfElse(b, c1, c2) =>
      var condition: bool;
      match b {
        case {:split false} Eq(x, y) =>
          condition := e.Eq(x, y);
        case {:split false} Elem(x, y) =>
          condition := e.Elem(x, y);
      }
      if condition {
        bigstep_level5(c1, e);
      } else {
        bigstep_level5(c2, e);
      }
    case {:split false} Seq(c1, c2) =>
      bigstep_level5(c1, e);
      bigstep_level5(c2, e);
  }
}

predicate method isInt(a: char)
  decreases a
{
  a as int - '0' as int <= 9
}

function method charToInt(a: char): int
  requires isInt(a)
  decreases a
{
  a as int - '0' as int
}

function method intToChar(a: nat): char
  requires a <= 9
  decreases a
{
  a as char + '0' as char
}

method strToInt(a: string) returns (r: Maybe<int>)
  requires |a| > 0
  ensures (forall k: int :: 0 <= k < |a| ==> isInt(a[k])) ==> exists x: int :: r == Just(x)
  ensures (exists k: int :: 0 <= k < |a| && !isInt(a[k])) ==> r == Nothing
  decreases a
{
  if isInt(a[0]) {
    r := Just(charToInt(a[0]));
  } else {
    r := Nothing;
  }
  assert !isInt(a[0]) ==> r == Nothing;
  for j: int := 1 to |a|
    invariant (forall k: int :: 0 <= k < |a| ==> isInt(a[k])) ==> exists x: int :: r == Just(x)
    invariant forall k: int :: 0 <= k < j ==> !isInt(a[k]) ==> r == Nothing
  {
    match r {
      case {:split false} Nothing() =>
        r := Nothing;
      case {:split false} Just(x) =>
        if isInt(a[j]) {
          r := Just(x * 10 + charToInt(a[j]));
        } else {
          r := Nothing;
        }
    }
  }
}

method intToStr(a: int) returns (r: string)
  decreases a
{
  r := """";
  var temp1 := a;
  while temp1 > 0
    decreases temp1
  {
    var temp2 := temp1 % 10;
    r := [intToChar(temp2)] + r;
    temp1 := (temp1 - temp2) / 10;
  }
}
")]

//-----------------------------------------------------------------------------
//
// Copyright by the contributors to the Dafny Project
// SPDX-License-Identifier: MIT
//
//-----------------------------------------------------------------------------

#if ISDAFNYRUNTIMELIB
using System; // for Func
using System.Numerics;
#endif

namespace DafnyAssembly {
  [AttributeUsage(AttributeTargets.Assembly)]
  public class DafnySourceAttribute : Attribute {
    public readonly string dafnySourceText;
    public DafnySourceAttribute(string txt) { dafnySourceText = txt; }
  }
}

namespace Dafny {
  using System.Collections.Generic;
  using System.Collections.Immutable;
  using System.Linq;

  public interface ISet<out T> {
    int Count { get; }
    long LongCount { get; }
    IEnumerable<T> Elements { get; }
    IEnumerable<ISet<T>> AllSubsets { get; }
    bool Contains<G>(G t);
    bool EqualsAux(ISet<object> other);
    ISet<U> DowncastClone<U>(Func<T, U> converter);
  }

  public class Set<T> : ISet<T> {
    readonly ImmutableHashSet<T> setImpl;
    readonly bool containsNull;
    Set(ImmutableHashSet<T> d, bool containsNull) {
      this.setImpl = d;
      this.containsNull = containsNull;
    }

    public static readonly ISet<T> Empty = new Set<T>(ImmutableHashSet<T>.Empty, false);

    private static readonly TypeDescriptor<ISet<T>> _TYPE = new Dafny.TypeDescriptor<ISet<T>>(Empty);
    public static TypeDescriptor<ISet<T>> _TypeDescriptor() {
      return _TYPE;
    }

    public static ISet<T> FromElements(params T[] values) {
      return FromCollection(values);
    }

    public static Set<T> FromISet(ISet<T> s) {
      return s as Set<T> ?? FromCollection(s.Elements);
    }

    public static Set<T> FromCollection(IEnumerable<T> values) {
      var d = ImmutableHashSet<T>.Empty.ToBuilder();
      var containsNull = false;
      foreach (T t in values) {
        if (t == null) {
          containsNull = true;
        } else {
          d.Add(t);
        }
      }

      return new Set<T>(d.ToImmutable(), containsNull);
    }

    public static ISet<T> FromCollectionPlusOne(IEnumerable<T> values, T oneMoreValue) {
      var d = ImmutableHashSet<T>.Empty.ToBuilder();
      var containsNull = false;
      if (oneMoreValue == null) {
        containsNull = true;
      } else {
        d.Add(oneMoreValue);
      }

      foreach (T t in values) {
        if (t == null) {
          containsNull = true;
        } else {
          d.Add(t);
        }
      }

      return new Set<T>(d.ToImmutable(), containsNull);
    }

    public ISet<U> DowncastClone<U>(Func<T, U> converter) {
      if (this is ISet<U> th) {
        return th;
      } else {
        var d = ImmutableHashSet<U>.Empty.ToBuilder();
        foreach (var t in this.setImpl) {
          var u = converter(t);
          d.Add(u);
        }

        return new Set<U>(d.ToImmutable(), this.containsNull);
      }
    }

    public int Count {
      get { return this.setImpl.Count + (containsNull ? 1 : 0); }
    }

    public long LongCount {
      get { return this.setImpl.Count + (containsNull ? 1 : 0); }
    }

    public IEnumerable<T> Elements {
      get {
        if (containsNull) {
          yield return default(T);
        }

        foreach (var t in this.setImpl) {
          yield return t;
        }
      }
    }

    /// <summary>
    /// This is an inefficient iterator for producing all subsets of "this".
    /// </summary>
    public IEnumerable<ISet<T>> AllSubsets {
      get {
        // Start by putting all set elements into a list, but don't include null
        var elmts = new List<T>();
        elmts.AddRange(this.setImpl);
        var n = elmts.Count;
        var which = new bool[n];
        var s = ImmutableHashSet<T>.Empty.ToBuilder();
        while (true) {
          // yield both the subset without null and, if null is in the original set, the subset with null included
          var ihs = s.ToImmutable();
          yield return new Set<T>(ihs, false);
          if (containsNull) {
            yield return new Set<T>(ihs, true);
          }

          // "add 1" to "which", as if doing a carry chain.  For every digit changed, change the membership of the corresponding element in "s".
          int i = 0;
          for (; i < n && which[i]; i++) {
            which[i] = false;
            s.Remove(elmts[i]);
          }

          if (i == n) {
            // we have cycled through all the subsets
            break;
          }

          which[i] = true;
          s.Add(elmts[i]);
        }
      }
    }

    public bool Equals(ISet<T> other) {
      if (other == null || Count != other.Count) {
        return false;
      } else if (this == other) {
        return true;
      }

      foreach (var elmt in Elements) {
        if (!other.Contains(elmt)) {
          return false;
        }
      }

      return true;
    }

    public override bool Equals(object other) {
      if (other is ISet<T>) {
        return Equals((ISet<T>)other);
      }

      var th = this as ISet<object>;
      var oth = other as ISet<object>;
      if (th != null && oth != null) {
        // We'd like to obtain the more specific type parameter U for oth's type ISet<U>.
        // We do that by making a dynamically dispatched call, like:
        //     oth.Equals(this)
        // The hope is then that its comparison "this is ISet<U>" (that is, the first "if" test
        // above, but in the call "oth.Equals(this)") will be true and the non-virtual Equals
        // can be called. However, such a recursive call to "oth.Equals(this)" could turn
        // into infinite recursion. Therefore, we instead call "oth.EqualsAux(this)", which
        // performs the desired type test, but doesn't recurse any further.
        return oth.EqualsAux(th);
      } else {
        return false;
      }
    }

    public bool EqualsAux(ISet<object> other) {
      var s = other as ISet<T>;
      if (s != null) {
        return Equals(s);
      } else {
        return false;
      }
    }

    public override int GetHashCode() {
      var hashCode = 1;
      if (containsNull) {
        hashCode = hashCode * (Dafny.Helpers.GetHashCode(default(T)) + 3);
      }

      foreach (var t in this.setImpl) {
        hashCode = hashCode * (Dafny.Helpers.GetHashCode(t) + 3);
      }

      return hashCode;
    }

    public override string ToString() {
      var s = "{";
      var sep = "";
      if (containsNull) {
        s += sep + Dafny.Helpers.ToString(default(T));
        sep = ", ";
      }

      foreach (var t in this.setImpl) {
        s += sep + Dafny.Helpers.ToString(t);
        sep = ", ";
      }

      return s + "}";
    }
    public static bool IsProperSubsetOf(ISet<T> th, ISet<T> other) {
      return th.Count < other.Count && IsSubsetOf(th, other);
    }
    public static bool IsSubsetOf(ISet<T> th, ISet<T> other) {
      if (other.Count < th.Count) {
        return false;
      }
      foreach (T t in th.Elements) {
        if (!other.Contains(t)) {
          return false;
        }
      }
      return true;
    }
    public static bool IsDisjointFrom(ISet<T> th, ISet<T> other) {
      ISet<T> a, b;
      if (th.Count < other.Count) {
        a = th; b = other;
      } else {
        a = other; b = th;
      }
      foreach (T t in a.Elements) {
        if (b.Contains(t)) {
          return false;
        }
      }
      return true;
    }
    public bool Contains<G>(G t) {
      return t == null ? containsNull : t is T && this.setImpl.Contains((T)(object)t);
    }
    public static ISet<T> Union(ISet<T> th, ISet<T> other) {
      var a = FromISet(th);
      var b = FromISet(other);
      return new Set<T>(a.setImpl.Union(b.setImpl), a.containsNull || b.containsNull);
    }
    public static ISet<T> Intersect(ISet<T> th, ISet<T> other) {
      var a = FromISet(th);
      var b = FromISet(other);
      return new Set<T>(a.setImpl.Intersect(b.setImpl), a.containsNull && b.containsNull);
    }
    public static ISet<T> Difference(ISet<T> th, ISet<T> other) {
      var a = FromISet(th);
      var b = FromISet(other);
      return new Set<T>(a.setImpl.Except(b.setImpl), a.containsNull && !b.containsNull);
    }
  }

  public interface IMultiSet<out T> {
    bool IsEmpty { get; }
    int Count { get; }
    long LongCount { get; }
    IEnumerable<T> Elements { get; }
    IEnumerable<T> UniqueElements { get; }
    bool Contains<G>(G t);
    BigInteger Select<G>(G t);
    IMultiSet<T> Update<G>(G t, BigInteger i);
    bool EqualsAux(IMultiSet<object> other);
    IMultiSet<U> DowncastClone<U>(Func<T, U> converter);
  }

  public class MultiSet<T> : IMultiSet<T> {
    readonly ImmutableDictionary<T, BigInteger> dict;
    readonly BigInteger occurrencesOfNull;  // stupidly, a Dictionary in .NET cannot use "null" as a key
    MultiSet(ImmutableDictionary<T, BigInteger>.Builder d, BigInteger occurrencesOfNull) {
      dict = d.ToImmutable();
      this.occurrencesOfNull = occurrencesOfNull;
    }
    public static readonly MultiSet<T> Empty = new MultiSet<T>(ImmutableDictionary<T, BigInteger>.Empty.ToBuilder(), BigInteger.Zero);

    private static readonly TypeDescriptor<IMultiSet<T>> _TYPE = new Dafny.TypeDescriptor<IMultiSet<T>>(Empty);
    public static TypeDescriptor<IMultiSet<T>> _TypeDescriptor() {
      return _TYPE;
    }

    public static MultiSet<T> FromIMultiSet(IMultiSet<T> s) {
      return s as MultiSet<T> ?? FromCollection(s.Elements);
    }
    public static MultiSet<T> FromElements(params T[] values) {
      var d = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      var occurrencesOfNull = BigInteger.Zero;
      foreach (T t in values) {
        if (t == null) {
          occurrencesOfNull++;
        } else {
          BigInteger i;
          if (!d.TryGetValue(t, out i)) {
            i = BigInteger.Zero;
          }
          d[t] = i + 1;
        }
      }
      return new MultiSet<T>(d, occurrencesOfNull);
    }

    public static MultiSet<T> FromCollection(IEnumerable<T> values) {
      var d = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      var occurrencesOfNull = BigInteger.Zero;
      foreach (T t in values) {
        if (t == null) {
          occurrencesOfNull++;
        } else {
          BigInteger i;
          if (!d.TryGetValue(t,
            out i)) {
            i = BigInteger.Zero;
          }

          d[t] = i + 1;
        }
      }

      return new MultiSet<T>(d,
        occurrencesOfNull);
    }

    public static MultiSet<T> FromSeq(ISequence<T> values) {
      var d = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      var occurrencesOfNull = BigInteger.Zero;
      foreach (T t in values.Elements) {
        if (t == null) {
          occurrencesOfNull++;
        } else {
          BigInteger i;
          if (!d.TryGetValue(t,
            out i)) {
            i = BigInteger.Zero;
          }

          d[t] = i + 1;
        }
      }

      return new MultiSet<T>(d,
        occurrencesOfNull);
    }
    public static MultiSet<T> FromSet(ISet<T> values) {
      var d = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      var containsNull = false;
      foreach (T t in values.Elements) {
        if (t == null) {
          containsNull = true;
        } else {
          d[t] = BigInteger.One;
        }
      }
      return new MultiSet<T>(d, containsNull ? BigInteger.One : BigInteger.Zero);
    }
    public IMultiSet<U> DowncastClone<U>(Func<T, U> converter) {
      if (this is IMultiSet<U> th) {
        return th;
      } else {
        var d = ImmutableDictionary<U, BigInteger>.Empty.ToBuilder();
        foreach (var item in this.dict) {
          var k = converter(item.Key);
          d.Add(k, item.Value);
        }
        return new MultiSet<U>(d, this.occurrencesOfNull);
      }
    }

    public bool Equals(IMultiSet<T> other) {
      return IsSubsetOf(this, other) && IsSubsetOf(other, this);
    }
    public override bool Equals(object other) {
      if (other is IMultiSet<T>) {
        return Equals((IMultiSet<T>)other);
      }
      var th = this as IMultiSet<object>;
      var oth = other as IMultiSet<object>;
      if (th != null && oth != null) {
        // See comment in Set.Equals
        return oth.EqualsAux(th);
      } else {
        return false;
      }
    }

    public bool EqualsAux(IMultiSet<object> other) {
      var s = other as IMultiSet<T>;
      if (s != null) {
        return Equals(s);
      } else {
        return false;
      }
    }

    public override int GetHashCode() {
      var hashCode = 1;
      if (occurrencesOfNull > 0) {
        var key = Dafny.Helpers.GetHashCode(default(T));
        key = (key << 3) | (key >> 29) ^ occurrencesOfNull.GetHashCode();
        hashCode = hashCode * (key + 3);
      }
      foreach (var kv in dict) {
        var key = Dafny.Helpers.GetHashCode(kv.Key);
        key = (key << 3) | (key >> 29) ^ kv.Value.GetHashCode();
        hashCode = hashCode * (key + 3);
      }
      return hashCode;
    }
    public override string ToString() {
      var s = "multiset{";
      var sep = "";
      for (var i = BigInteger.Zero; i < occurrencesOfNull; i++) {
        s += sep + Dafny.Helpers.ToString(default(T));
        sep = ", ";
      }
      foreach (var kv in dict) {
        var t = Dafny.Helpers.ToString(kv.Key);
        for (var i = BigInteger.Zero; i < kv.Value; i++) {
          s += sep + t;
          sep = ", ";
        }
      }
      return s + "}";
    }
    public static bool IsProperSubsetOf(IMultiSet<T> th, IMultiSet<T> other) {
      return th.Count < other.Count && IsSubsetOf(th, other);
    }
    public static bool IsSubsetOf(IMultiSet<T> th, IMultiSet<T> other) {
      var a = FromIMultiSet(th);
      var b = FromIMultiSet(other);
      if (b.occurrencesOfNull < a.occurrencesOfNull) {
        return false;
      }
      foreach (T t in a.dict.Keys) {
        if (b.dict.ContainsKey(t)) {
          if (b.dict[t] < a.dict[t]) {
            return false;
          }
        } else {
          if (a.dict[t] != BigInteger.Zero) {
            return false;
          }
        }
      }
      return true;
    }
    public static bool IsDisjointFrom(IMultiSet<T> th, IMultiSet<T> other) {
      foreach (T t in th.UniqueElements) {
        if (other.Contains(t)) {
          return false;
        }
      }
      return true;
    }

    public bool Contains<G>(G t) {
      return Select(t) != 0;
    }
    public BigInteger Select<G>(G t) {
      if (t == null) {
        return occurrencesOfNull;
      }
      BigInteger m;
      if (t is T && dict.TryGetValue((T)(object)t, out m)) {
        return m;
      } else {
        return BigInteger.Zero;
      }
    }
    public IMultiSet<T> Update<G>(G t, BigInteger i) {
      if (Select(t) == i) {
        return this;
      } else if (t == null) {
        var r = dict.ToBuilder();
        return new MultiSet<T>(r, i);
      } else {
        var r = dict.ToBuilder();
        r[(T)(object)t] = i;
        return new MultiSet<T>(r, occurrencesOfNull);
      }
    }
    public static IMultiSet<T> Union(IMultiSet<T> th, IMultiSet<T> other) {
      if (th.IsEmpty) {
        return other;
      } else if (other.IsEmpty) {
        return th;
      }
      var a = FromIMultiSet(th);
      var b = FromIMultiSet(other);
      var r = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      foreach (T t in a.dict.Keys) {
        BigInteger i;
        if (!r.TryGetValue(t, out i)) {
          i = BigInteger.Zero;
        }
        r[t] = i + a.dict[t];
      }
      foreach (T t in b.dict.Keys) {
        BigInteger i;
        if (!r.TryGetValue(t, out i)) {
          i = BigInteger.Zero;
        }
        r[t] = i + b.dict[t];
      }
      return new MultiSet<T>(r, a.occurrencesOfNull + b.occurrencesOfNull);
    }
    public static IMultiSet<T> Intersect(IMultiSet<T> th, IMultiSet<T> other) {
      if (th.IsEmpty) {
        return th;
      } else if (other.IsEmpty) {
        return other;
      }
      var a = FromIMultiSet(th);
      var b = FromIMultiSet(other);
      var r = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      foreach (T t in a.dict.Keys) {
        if (b.dict.ContainsKey(t)) {
          r.Add(t, a.dict[t] < b.dict[t] ? a.dict[t] : b.dict[t]);
        }
      }
      return new MultiSet<T>(r, a.occurrencesOfNull < b.occurrencesOfNull ? a.occurrencesOfNull : b.occurrencesOfNull);
    }
    public static IMultiSet<T> Difference(IMultiSet<T> th, IMultiSet<T> other) { // \result == this - other
      if (other.IsEmpty) {
        return th;
      }
      var a = FromIMultiSet(th);
      var b = FromIMultiSet(other);
      var r = ImmutableDictionary<T, BigInteger>.Empty.ToBuilder();
      foreach (T t in a.dict.Keys) {
        if (!b.dict.ContainsKey(t)) {
          r.Add(t, a.dict[t]);
        } else if (b.dict[t] < a.dict[t]) {
          r.Add(t, a.dict[t] - b.dict[t]);
        }
      }
      return new MultiSet<T>(r, b.occurrencesOfNull < a.occurrencesOfNull ? a.occurrencesOfNull - b.occurrencesOfNull : BigInteger.Zero);
    }

    public bool IsEmpty { get { return occurrencesOfNull == 0 && dict.IsEmpty; } }

    public int Count {
      get { return (int)ElementCount(); }
    }
    public long LongCount {
      get { return (long)ElementCount(); }
    }
    private BigInteger ElementCount() {
      // This is inefficient
      var c = occurrencesOfNull;
      foreach (var item in dict) {
        c += item.Value;
      }
      return c;
    }

    public IEnumerable<T> Elements {
      get {
        for (var i = BigInteger.Zero; i < occurrencesOfNull; i++) {
          yield return default(T);
        }
        foreach (var item in dict) {
          for (var i = BigInteger.Zero; i < item.Value; i++) {
            yield return item.Key;
          }
        }
      }
    }

    public IEnumerable<T> UniqueElements {
      get {
        if (!occurrencesOfNull.IsZero) {
          yield return default(T);
        }
        foreach (var key in dict.Keys) {
          if (dict[key] != 0) {
            yield return key;
          }
        }
      }
    }
  }

  public interface IMap<out U, out V> {
    int Count { get; }
    long LongCount { get; }
    ISet<U> Keys { get; }
    ISet<V> Values { get; }
    IEnumerable<IPair<U, V>> ItemEnumerable { get; }
    bool Contains<G>(G t);
    /// <summary>
    /// Returns "true" iff "this is IMap<object, object>" and "this" equals "other".
    /// </summary>
    bool EqualsObjObj(IMap<object, object> other);
    IMap<UU, VV> DowncastClone<UU, VV>(Func<U, UU> keyConverter, Func<V, VV> valueConverter);
  }

  public class Map<U, V> : IMap<U, V> {
    readonly ImmutableDictionary<U, V> dict;
    readonly bool hasNullKey;  // true when "null" is a key of the Map
    readonly V nullValue;  // if "hasNullKey", the value that "null" maps to

    private Map(ImmutableDictionary<U, V>.Builder d, bool hasNullKey, V nullValue) {
      dict = d.ToImmutable();
      this.hasNullKey = hasNullKey;
      this.nullValue = nullValue;
    }
    public static readonly Map<U, V> Empty = new Map<U, V>(ImmutableDictionary<U, V>.Empty.ToBuilder(), false, default(V));

    private Map(ImmutableDictionary<U, V> d, bool hasNullKey, V nullValue) {
      dict = d;
      this.hasNullKey = hasNullKey;
      this.nullValue = nullValue;
    }

    private static readonly TypeDescriptor<IMap<U, V>> _TYPE = new Dafny.TypeDescriptor<IMap<U, V>>(Empty);
    public static TypeDescriptor<IMap<U, V>> _TypeDescriptor() {
      return _TYPE;
    }

    public static Map<U, V> FromElements(params IPair<U, V>[] values) {
      var d = ImmutableDictionary<U, V>.Empty.ToBuilder();
      var hasNullKey = false;
      var nullValue = default(V);
      foreach (var p in values) {
        if (p.Car == null) {
          hasNullKey = true;
          nullValue = p.Cdr;
        } else {
          d[p.Car] = p.Cdr;
        }
      }
      return new Map<U, V>(d, hasNullKey, nullValue);
    }
    public static Map<U, V> FromCollection(IEnumerable<IPair<U, V>> values) {
      var d = ImmutableDictionary<U, V>.Empty.ToBuilder();
      var hasNullKey = false;
      var nullValue = default(V);
      foreach (var p in values) {
        if (p.Car == null) {
          hasNullKey = true;
          nullValue = p.Cdr;
        } else {
          d[p.Car] = p.Cdr;
        }
      }
      return new Map<U, V>(d, hasNullKey, nullValue);
    }
    public static Map<U, V> FromIMap(IMap<U, V> m) {
      return m as Map<U, V> ?? FromCollection(m.ItemEnumerable);
    }
    public IMap<UU, VV> DowncastClone<UU, VV>(Func<U, UU> keyConverter, Func<V, VV> valueConverter) {
      if (this is IMap<UU, VV> th) {
        return th;
      } else {
        var d = ImmutableDictionary<UU, VV>.Empty.ToBuilder();
        foreach (var item in this.dict) {
          var k = keyConverter(item.Key);
          var v = valueConverter(item.Value);
          d.Add(k, v);
        }
        return new Map<UU, VV>(d, this.hasNullKey, (VV)(object)this.nullValue);
      }
    }
    public int Count {
      get { return dict.Count + (hasNullKey ? 1 : 0); }
    }
    public long LongCount {
      get { return dict.Count + (hasNullKey ? 1 : 0); }
    }

    public bool Equals(IMap<U, V> other) {
      if (other == null || LongCount != other.LongCount) {
        return false;
      } else if (this == other) {
        return true;
      }
      if (hasNullKey) {
        if (!other.Contains(default(U)) || !object.Equals(nullValue, Select(other, default(U)))) {
          return false;
        }
      }
      foreach (var item in dict) {
        if (!other.Contains(item.Key) || !object.Equals(item.Value, Select(other, item.Key))) {
          return false;
        }
      }
      return true;
    }
    public bool EqualsObjObj(IMap<object, object> other) {
      if (!(this is IMap<object, object>) || other == null || LongCount != other.LongCount) {
        return false;
      } else if (this == other) {
        return true;
      }
      var oth = Map<object, object>.FromIMap(other);
      if (hasNullKey) {
        if (!oth.Contains(default(U)) || !object.Equals(nullValue, Map<object, object>.Select(oth, default(U)))) {
          return false;
        }
      }
      foreach (var item in dict) {
        if (!other.Contains(item.Key) || !object.Equals(item.Value, Map<object, object>.Select(oth, item.Key))) {
          return false;
        }
      }
      return true;
    }
    public override bool Equals(object other) {
      // See comment in Set.Equals
      var m = other as IMap<U, V>;
      if (m != null) {
        return Equals(m);
      }
      var imapoo = other as IMap<object, object>;
      if (imapoo != null) {
        return EqualsObjObj(imapoo);
      } else {
        return false;
      }
    }

    public override int GetHashCode() {
      var hashCode = 1;
      if (hasNullKey) {
        var key = Dafny.Helpers.GetHashCode(default(U));
        key = (key << 3) | (key >> 29) ^ Dafny.Helpers.GetHashCode(nullValue);
        hashCode = hashCode * (key + 3);
      }
      foreach (var kv in dict) {
        var key = Dafny.Helpers.GetHashCode(kv.Key);
        key = (key << 3) | (key >> 29) ^ Dafny.Helpers.GetHashCode(kv.Value);
        hashCode = hashCode * (key + 3);
      }
      return hashCode;
    }
    public override string ToString() {
      var s = "map[";
      var sep = "";
      if (hasNullKey) {
        s += sep + Dafny.Helpers.ToString(default(U)) + " := " + Dafny.Helpers.ToString(nullValue);
        sep = ", ";
      }
      foreach (var kv in dict) {
        s += sep + Dafny.Helpers.ToString(kv.Key) + " := " + Dafny.Helpers.ToString(kv.Value);
        sep = ", ";
      }
      return s + "]";
    }
    public bool Contains<G>(G u) {
      return u == null ? hasNullKey : u is U && dict.ContainsKey((U)(object)u);
    }
    public static V Select(IMap<U, V> th, U index) {
      // the following will throw an exception if "index" in not a key of the map
      var m = FromIMap(th);
      return index == null && m.hasNullKey ? m.nullValue : m.dict[index];
    }
    public static IMap<U, V> Update(IMap<U, V> th, U index, V val) {
      var m = FromIMap(th);
      var d = m.dict.ToBuilder();
      if (index == null) {
        return new Map<U, V>(d, true, val);
      } else {
        d[index] = val;
        return new Map<U, V>(d, m.hasNullKey, m.nullValue);
      }
    }

    public static IMap<U, V> Merge(IMap<U, V> th, IMap<U, V> other) {
      var a = FromIMap(th);
      var b = FromIMap(other);
      ImmutableDictionary<U, V> d = a.dict.SetItems(b.dict);
      return new Map<U, V>(d, a.hasNullKey || b.hasNullKey, b.hasNullKey ? b.nullValue : a.nullValue);
    }

    public static IMap<U, V> Subtract(IMap<U, V> th, ISet<U> keys) {
      var a = FromIMap(th);
      ImmutableDictionary<U, V> d = a.dict.RemoveRange(keys.Elements);
      return new Map<U, V>(d, a.hasNullKey && !keys.Contains<object>(null), a.nullValue);
    }

    public ISet<U> Keys {
      get {
        if (hasNullKey) {
          return Dafny.Set<U>.FromCollectionPlusOne(dict.Keys, default(U));
        } else {
          return Dafny.Set<U>.FromCollection(dict.Keys);
        }
      }
    }
    public ISet<V> Values {
      get {
        if (hasNullKey) {
          return Dafny.Set<V>.FromCollectionPlusOne(dict.Values, nullValue);
        } else {
          return Dafny.Set<V>.FromCollection(dict.Values);
        }
      }
    }

    public IEnumerable<IPair<U, V>> ItemEnumerable {
      get {
        if (hasNullKey) {
          yield return new Pair<U, V>(default(U), nullValue);
        }
        foreach (KeyValuePair<U, V> kvp in dict) {
          yield return new Pair<U, V>(kvp.Key, kvp.Value);
        }
      }
    }

    public static ISet<_System._ITuple2<U, V>> Items(IMap<U, V> m) {
      var result = new HashSet<_System._ITuple2<U, V>>();
      foreach (var item in m.ItemEnumerable) {
        result.Add(_System.Tuple2<U, V>.create(item.Car, item.Cdr));
      }
      return Dafny.Set<_System._ITuple2<U, V>>.FromCollection(result);
    }
  }

  public interface ISequence<out T> {
    long LongCount { get; }
    int Count { get; }
    T[] Elements { get; }
    IEnumerable<T> UniqueElements { get; }
    T Select(ulong index);
    T Select(long index);
    T Select(uint index);
    T Select(int index);
    T Select(BigInteger index);
    bool Contains<G>(G g);
    ISequence<T> Take(long m);
    ISequence<T> Take(ulong n);
    ISequence<T> Take(BigInteger n);
    ISequence<T> Drop(long m);
    ISequence<T> Drop(ulong n);
    ISequence<T> Drop(BigInteger n);
    ISequence<T> Subsequence(long lo, long hi);
    ISequence<T> Subsequence(long lo, ulong hi);
    ISequence<T> Subsequence(long lo, BigInteger hi);
    ISequence<T> Subsequence(ulong lo, long hi);
    ISequence<T> Subsequence(ulong lo, ulong hi);
    ISequence<T> Subsequence(ulong lo, BigInteger hi);
    ISequence<T> Subsequence(BigInteger lo, long hi);
    ISequence<T> Subsequence(BigInteger lo, ulong hi);
    ISequence<T> Subsequence(BigInteger lo, BigInteger hi);
    bool EqualsAux(ISequence<object> other);
    ISequence<U> DowncastClone<U>(Func<T, U> converter);
  }

  public abstract class Sequence<T> : ISequence<T> {
    public static readonly ISequence<T> Empty = new ArraySequence<T>(new T[0]);

    private static readonly TypeDescriptor<ISequence<T>> _TYPE = new Dafny.TypeDescriptor<ISequence<T>>(Empty);
    public static TypeDescriptor<ISequence<T>> _TypeDescriptor() {
      return _TYPE;
    }

    public static ISequence<T> Create(BigInteger length, System.Func<BigInteger, T> init) {
      var len = (int)length;
      var values = new T[len];
      for (int i = 0; i < len; i++) {
        values[i] = init(new BigInteger(i));
      }
      return new ArraySequence<T>(values);
    }
    public static ISequence<T> FromArray(T[] values) {
      return new ArraySequence<T>(values);
    }
    public static ISequence<T> FromElements(params T[] values) {
      return new ArraySequence<T>(values);
    }
    public static ISequence<char> FromString(string s) {
      return new ArraySequence<char>(s.ToCharArray());
    }
    public ISequence<U> DowncastClone<U>(Func<T, U> converter) {
      if (this is ISequence<U> th) {
        return th;
      } else {
        var values = new U[this.LongCount];
        for (long i = 0; i < this.LongCount; i++) {
          var val = converter(this.Select(i));
          values[i] = val;
        }
        return new ArraySequence<U>(values);
      }
    }
    public static ISequence<T> Update(ISequence<T> sequence, long index, T t) {
      T[] tmp = (T[])sequence.Elements.Clone();
      tmp[index] = t;
      return new ArraySequence<T>(tmp);
    }
    public static ISequence<T> Update(ISequence<T> sequence, ulong index, T t) {
      return Update(sequence, (long)index, t);
    }
    public static ISequence<T> Update(ISequence<T> sequence, BigInteger index, T t) {
      return Update(sequence, (long)index, t);
    }
    public static bool EqualUntil(ISequence<T> left, ISequence<T> right, int n) {
      T[] leftElmts = left.Elements, rightElmts = right.Elements;
      for (int i = 0; i < n; i++) {
        if (!object.Equals(leftElmts[i], rightElmts[i])) {
          return false;
        }
      }
      return true;
    }
    public static bool IsPrefixOf(ISequence<T> left, ISequence<T> right) {
      int n = left.Elements.Length;
      return n <= right.Elements.Length && EqualUntil(left, right, n);
    }
    public static bool IsProperPrefixOf(ISequence<T> left, ISequence<T> right) {
      int n = left.Elements.Length;
      return n < right.Elements.Length && EqualUntil(left, right, n);
    }
    public static ISequence<T> Concat(ISequence<T> left, ISequence<T> right) {
      if (left.Count == 0) {
        return right;
      }
      if (right.Count == 0) {
        return left;
      }
      return new ConcatSequence<T>(left, right);
    }
    // Make Count a public abstract instead of LongCount, since the "array size is limited to a total of 4 billion
    // elements, and to a maximum index of 0X7FEFFFFF". Therefore, as a protection, limit this to int32.
    // https://docs.microsoft.com/en-us/dotnet/api/system.array
    public abstract int Count { get; }
    public long LongCount {
      get { return Count; }
    }
    // ImmutableElements cannot be public in the interface since ImmutableArray<T> leads to a
    // "covariant type T occurs in invariant position" error. There do not appear to be interfaces for ImmutableArray<T>
    // that resolve this.
    protected abstract ImmutableArray<T> ImmutableElements { get; }

    public T[] Elements {
      get { return ImmutableElements.ToArray(); }
    }
    public IEnumerable<T> UniqueElements {
      get {
        var st = Set<T>.FromCollection(ImmutableElements);
        return st.Elements;
      }
    }

    public T Select(ulong index) {
      return ImmutableElements[checked((int)index)];
    }
    public T Select(long index) {
      return ImmutableElements[checked((int)index)];
    }
    public T Select(uint index) {
      return ImmutableElements[checked((int)index)];
    }
    public T Select(int index) {
      return ImmutableElements[index];
    }
    public T Select(BigInteger index) {
      return ImmutableElements[(int)index];
    }
    public bool Equals(ISequence<T> other) {
      int n = ImmutableElements.Length;
      return n == other.Elements.Length && EqualUntil(this, other, n);
    }
    public override bool Equals(object other) {
      if (other is ISequence<T>) {
        return Equals((ISequence<T>)other);
      }
      var th = this as ISequence<object>;
      var oth = other as ISequence<object>;
      if (th != null && oth != null) {
        // see explanation in Set.Equals
        return oth.EqualsAux(th);
      } else {
        return false;
      }
    }
    public bool EqualsAux(ISequence<object> other) {
      var s = other as ISequence<T>;
      if (s != null) {
        return Equals(s);
      } else {
        return false;
      }
    }
    public override int GetHashCode() {
      ImmutableArray<T> elmts = ImmutableElements;
      // https://devblogs.microsoft.com/dotnet/please-welcome-immutablearrayt/
      if (elmts.IsDefaultOrEmpty) {
        return 0;
      }

      var hashCode = 0;
      for (var i = 0; i < elmts.Length; i++) {
        hashCode = (hashCode << 3) | (hashCode >> 29) ^ Dafny.Helpers.GetHashCode(elmts[i]);
      }
      return hashCode;
    }
    public override string ToString() {
      // This is required because (ImmutableElements is ImmutableArray<char>) is not a valid type check
      var typeCheckTmp = new T[0];
      ImmutableArray<T> elmts = ImmutableElements;
      if (typeCheckTmp is char[]) {
        var s = "";
        foreach (var t in elmts) {
          s += t.ToString();
        }
        return s;
      } else {
        var s = "[";
        var sep = "";
        foreach (var t in elmts) {
          s += sep + Dafny.Helpers.ToString(t);
          sep = ", ";
        }
        return s + "]";
      }
    }
    public bool Contains<G>(G g) {
      if (g == null || g is T) {
        var t = (T)(object)g;
        return ImmutableElements.Contains(t);
      }
      return false;
    }
    public ISequence<T> Take(long m) {
      if (ImmutableElements.Length == m) {
        return this;
      }

      int length = checked((int)m);
      T[] tmp = new T[length];
      ImmutableElements.CopyTo(0, tmp, 0, length);
      return new ArraySequence<T>(tmp);
    }
    public ISequence<T> Take(ulong n) {
      return Take((long)n);
    }
    public ISequence<T> Take(BigInteger n) {
      return Take((long)n);
    }
    public ISequence<T> Drop(long m) {
      int startingElement = checked((int)m);
      if (startingElement == 0) {
        return this;
      }

      int length = ImmutableElements.Length - startingElement;
      T[] tmp = new T[length];
      ImmutableElements.CopyTo(startingElement, tmp, 0, length);
      return new ArraySequence<T>(tmp);
    }
    public ISequence<T> Drop(ulong n) {
      return Drop((long)n);
    }
    public ISequence<T> Drop(BigInteger n) {
      if (n.IsZero) {
        return this;
      }

      return Drop((long)n);
    }
    public ISequence<T> Subsequence(long lo, long hi) {
      if (lo == 0 && hi == ImmutableElements.Length) {
        return this;
      }
      int startingIndex = checked((int)lo);
      int endingIndex = checked((int)hi);
      var length = endingIndex - startingIndex;
      T[] tmp = new T[length];
      ImmutableElements.CopyTo(startingIndex, tmp, 0, length);
      return new ArraySequence<T>(tmp);
    }
    public ISequence<T> Subsequence(long lo, ulong hi) {
      return Subsequence(lo, (long)hi);
    }
    public ISequence<T> Subsequence(long lo, BigInteger hi) {
      return Subsequence(lo, (long)hi);
    }
    public ISequence<T> Subsequence(ulong lo, long hi) {
      return Subsequence((long)lo, hi);
    }
    public ISequence<T> Subsequence(ulong lo, ulong hi) {
      return Subsequence((long)lo, (long)hi);
    }
    public ISequence<T> Subsequence(ulong lo, BigInteger hi) {
      return Subsequence((long)lo, (long)hi);
    }
    public ISequence<T> Subsequence(BigInteger lo, long hi) {
      return Subsequence((long)lo, hi);
    }
    public ISequence<T> Subsequence(BigInteger lo, ulong hi) {
      return Subsequence((long)lo, (long)hi);
    }
    public ISequence<T> Subsequence(BigInteger lo, BigInteger hi) {
      return Subsequence((long)lo, (long)hi);
    }
  }

  internal class ArraySequence<T> : Sequence<T> {
    private readonly ImmutableArray<T> elmts;

    internal ArraySequence(ImmutableArray<T> ee) {
      elmts = ee;
    }
    internal ArraySequence(T[] ee) {
      elmts = ImmutableArray.Create<T>(ee);
    }

    protected override ImmutableArray<T> ImmutableElements {
      get {
        return elmts;
      }
    }
    public override int Count {
      get {
        return elmts.Length;
      }
    }
  }

  internal class ConcatSequence<T> : Sequence<T> {
    // INVARIANT: Either left != null, right != null, and elmts's underlying array == null or
    // left == null, right == null, and elmts's underlying array != null
    private volatile ISequence<T> left, right;
    private ImmutableArray<T> elmts;
    private readonly int count;

    internal ConcatSequence(ISequence<T> left, ISequence<T> right) {
      this.left = left;
      this.right = right;
      this.count = left.Count + right.Count;
    }

    protected override ImmutableArray<T> ImmutableElements {
      get {
        // IsDefault returns true if the underlying array is a null reference
        // https://devblogs.microsoft.com/dotnet/please-welcome-immutablearrayt/
        if (elmts.IsDefault) {
          elmts = ComputeElements();
          // We don't need the original sequences anymore; let them be
          // garbage-collected
          left = null;
          right = null;
        }
        return elmts;
      }
    }

    public override int Count {
      get {
        return count;
      }
    }

    private ImmutableArray<T> ComputeElements() {
      // Traverse the tree formed by all descendants which are ConcatSequences
      var ansBuilder = ImmutableArray.CreateBuilder<T>();
      var toVisit = new Stack<ISequence<T>>();
      var (leftBuffer, rightBuffer) = (left, right);
      if (left == null || right == null) {
        // elmts can't be .IsDefault while either left, or right are null
        return elmts;
      }
      toVisit.Push(rightBuffer);
      toVisit.Push(leftBuffer);

      while (toVisit.Count != 0) {
        var seq = toVisit.Pop();
        if (seq is ConcatSequence<T> cs && cs.elmts.IsDefault) {
          (leftBuffer, rightBuffer) = (cs.left, cs.right);
          if (cs.left == null || cs.right == null) {
            // !cs.elmts.IsDefault, due to concurrent enumeration
            toVisit.Push(cs);
          } else {
            toVisit.Push(rightBuffer);
            toVisit.Push(leftBuffer);
          }
        } else {
          var array = seq.Elements;
          ansBuilder.AddRange(array);
        }
      }
      return ansBuilder.ToImmutable();
    }
  }

  public interface IPair<out A, out B> {
    A Car { get; }
    B Cdr { get; }
  }

  public class Pair<A, B> : IPair<A, B> {
    private A car;
    private B cdr;
    public A Car { get { return car; } }
    public B Cdr { get { return cdr; } }
    public Pair(A a, B b) {
      this.car = a;
      this.cdr = b;
    }
  }

  public class TypeDescriptor<T> {
    private readonly T initValue;
    public TypeDescriptor(T initValue) {
      this.initValue = initValue;
    }
    public T Default() {
      return initValue;
    }
  }

  public partial class Helpers {
    public static int GetHashCode<G>(G g) {
      return g == null ? 1001 : g.GetHashCode();
    }

    public static int ToIntChecked(BigInteger i, string msg) {
      if (i > Int32.MaxValue || i < Int32.MinValue) {
        if (msg == null) {
          msg = "value out of range for a 32-bit int";
        }

        throw new HaltException(msg + ": " + i);
      }
      return (int)i;
    }
    public static int ToIntChecked(long i, string msg) {
      if (i > Int32.MaxValue || i < Int32.MinValue) {
        if (msg == null) {
          msg = "value out of range for a 32-bit int";
        }

        throw new HaltException(msg + ": " + i);
      }
      return (int)i;
    }
    public static int ToIntChecked(int i, string msg) {
      return i;
    }

    public static string ToString<G>(G g) {
      if (g == null) {
        return "null";
      } else if (g is bool) {
        return (bool)(object)g ? "true" : "false";  // capitalize boolean literals like in Dafny
      } else {
        return g.ToString();
      }
    }
    public static void Print<G>(G g) {
      System.Console.Write(ToString(g));
    }

    public static readonly TypeDescriptor<bool> BOOL = new TypeDescriptor<bool>(false);
    public static readonly TypeDescriptor<char> CHAR = new TypeDescriptor<char>('D');  // See CharType.DefaultValue in Dafny source code
    public static readonly TypeDescriptor<BigInteger> INT = new TypeDescriptor<BigInteger>(BigInteger.Zero);
    public static readonly TypeDescriptor<BigRational> REAL = new TypeDescriptor<BigRational>(BigRational.ZERO);
    public static readonly TypeDescriptor<byte> UINT8 = new TypeDescriptor<byte>(0);
    public static readonly TypeDescriptor<ushort> UINT16 = new TypeDescriptor<ushort>(0);
    public static readonly TypeDescriptor<uint> UINT32 = new TypeDescriptor<uint>(0);
    public static readonly TypeDescriptor<ulong> UINT64 = new TypeDescriptor<ulong>(0);

    public static TypeDescriptor<T> NULL<T>() where T : class {
      return new TypeDescriptor<T>(null);
    }

    public static TypeDescriptor<A[]> ARRAY<A>() {
      return new TypeDescriptor<A[]>(new A[0]);
    }

    public static bool Quantifier<T>(IEnumerable<T> vals, bool frall, System.Predicate<T> pred) {
      foreach (var u in vals) {
        if (pred(u) != frall) { return !frall; }
      }
      return frall;
    }
    // Enumerating other collections
    public static IEnumerable<bool> AllBooleans() {
      yield return false;
      yield return true;
    }
    public static IEnumerable<char> AllChars() {
      for (int i = 0; i < 0x10000; i++) {
        yield return (char)i;
      }
    }
    public static IEnumerable<BigInteger> AllIntegers() {
      yield return new BigInteger(0);
      for (var j = new BigInteger(1); ; j++) {
        yield return j;
        yield return -j;
      }
    }
    public static IEnumerable<BigInteger> IntegerRange(Nullable<BigInteger> lo, Nullable<BigInteger> hi) {
      if (lo == null) {
        for (var j = (BigInteger)hi; true;) {
          j--;
          yield return j;
        }
      } else if (hi == null) {
        for (var j = (BigInteger)lo; true; j++) {
          yield return j;
        }
      } else {
        for (var j = (BigInteger)lo; j < hi; j++) {
          yield return j;
        }
      }
    }
    public static IEnumerable<T> SingleValue<T>(T e) {
      yield return e;
    }
    // pre: b != 0
    // post: result == a/b, as defined by Euclidean Division (http://en.wikipedia.org/wiki/Modulo_operation)
    public static sbyte EuclideanDivision_sbyte(sbyte a, sbyte b) {
      return (sbyte)EuclideanDivision_int(a, b);
    }
    public static short EuclideanDivision_short(short a, short b) {
      return (short)EuclideanDivision_int(a, b);
    }
    public static int EuclideanDivision_int(int a, int b) {
      if (0 <= a) {
        if (0 <= b) {
          // +a +b: a/b
          return (int)(((uint)(a)) / ((uint)(b)));
        } else {
          // +a -b: -(a/(-b))
          return -((int)(((uint)(a)) / ((uint)(unchecked(-b)))));
        }
      } else {
        if (0 <= b) {
          // -a +b: -((-a-1)/b) - 1
          return -((int)(((uint)(-(a + 1))) / ((uint)(b)))) - 1;
        } else {
          // -a -b: ((-a-1)/(-b)) + 1
          return ((int)(((uint)(-(a + 1))) / ((uint)(unchecked(-b))))) + 1;
        }
      }
    }
    public static long EuclideanDivision_long(long a, long b) {
      if (0 <= a) {
        if (0 <= b) {
          // +a +b: a/b
          return (long)(((ulong)(a)) / ((ulong)(b)));
        } else {
          // +a -b: -(a/(-b))
          return -((long)(((ulong)(a)) / ((ulong)(unchecked(-b)))));
        }
      } else {
        if (0 <= b) {
          // -a +b: -((-a-1)/b) - 1
          return -((long)(((ulong)(-(a + 1))) / ((ulong)(b)))) - 1;
        } else {
          // -a -b: ((-a-1)/(-b)) + 1
          return ((long)(((ulong)(-(a + 1))) / ((ulong)(unchecked(-b))))) + 1;
        }
      }
    }
    public static BigInteger EuclideanDivision(BigInteger a, BigInteger b) {
      if (0 <= a.Sign) {
        if (0 <= b.Sign) {
          // +a +b: a/b
          return BigInteger.Divide(a, b);
        } else {
          // +a -b: -(a/(-b))
          return BigInteger.Negate(BigInteger.Divide(a, BigInteger.Negate(b)));
        }
      } else {
        if (0 <= b.Sign) {
          // -a +b: -((-a-1)/b) - 1
          return BigInteger.Negate(BigInteger.Divide(BigInteger.Negate(a) - 1, b)) - 1;
        } else {
          // -a -b: ((-a-1)/(-b)) + 1
          return BigInteger.Divide(BigInteger.Negate(a) - 1, BigInteger.Negate(b)) + 1;
        }
      }
    }
    // pre: b != 0
    // post: result == a%b, as defined by Euclidean Division (http://en.wikipedia.org/wiki/Modulo_operation)
    public static sbyte EuclideanModulus_sbyte(sbyte a, sbyte b) {
      return (sbyte)EuclideanModulus_int(a, b);
    }
    public static short EuclideanModulus_short(short a, short b) {
      return (short)EuclideanModulus_int(a, b);
    }
    public static int EuclideanModulus_int(int a, int b) {
      uint bp = (0 <= b) ? (uint)b : (uint)(unchecked(-b));
      if (0 <= a) {
        // +a: a % b'
        return (int)(((uint)a) % bp);
      } else {
        // c = ((-a) % b')
        // -a: b' - c if c > 0
        // -a: 0 if c == 0
        uint c = ((uint)(unchecked(-a))) % bp;
        return (int)(c == 0 ? c : bp - c);
      }
    }
    public static long EuclideanModulus_long(long a, long b) {
      ulong bp = (0 <= b) ? (ulong)b : (ulong)(unchecked(-b));
      if (0 <= a) {
        // +a: a % b'
        return (long)(((ulong)a) % bp);
      } else {
        // c = ((-a) % b')
        // -a: b' - c if c > 0
        // -a: 0 if c == 0
        ulong c = ((ulong)(unchecked(-a))) % bp;
        return (long)(c == 0 ? c : bp - c);
      }
    }
    public static BigInteger EuclideanModulus(BigInteger a, BigInteger b) {
      var bp = BigInteger.Abs(b);
      if (0 <= a.Sign) {
        // +a: a % b'
        return BigInteger.Remainder(a, bp);
      } else {
        // c = ((-a) % b')
        // -a: b' - c if c > 0
        // -a: 0 if c == 0
        var c = BigInteger.Remainder(BigInteger.Negate(a), bp);
        return c.IsZero ? c : BigInteger.Subtract(bp, c);
      }
    }

    public static U CastConverter<T, U>(T t) {
      return (U)(object)t;
    }

    public static Sequence<T> SeqFromArray<T>(T[] array) {
      return new ArraySequence<T>((T[])array.Clone());
    }
    // In .NET version 4.5, it is possible to mark a method with "AggressiveInlining", which says to inline the
    // method if possible.  Method "ExpressionSequence" would be a good candidate for it:
    // [System.Runtime.CompilerServices.MethodImpl(System.Runtime.CompilerServices.MethodImplOptions.AggressiveInlining)]
    public static U ExpressionSequence<T, U>(T t, U u) {
      return u;
    }

    public static U Let<T, U>(T t, Func<T, U> f) {
      return f(t);
    }

    public static A Id<A>(A a) {
      return a;
    }

    public static void WithHaltHandling(Action action) {
      try {
        action();
      } catch (HaltException e) {
        Console.WriteLine("[Program halted] " + e.Message);
      }
    }
  }

  public class BigOrdinal {
    public static bool IsLimit(BigInteger ord) {
      return ord == 0;
    }
    public static bool IsSucc(BigInteger ord) {
      return 0 < ord;
    }
    public static BigInteger Offset(BigInteger ord) {
      return ord;
    }
    public static bool IsNat(BigInteger ord) {
      return true;  // at run time, every ORDINAL is a natural number
    }
  }

  public struct BigRational {
    public static readonly BigRational ZERO = new BigRational(0);

    // We need to deal with the special case "num == 0 && den == 0", because
    // that's what C#'s default struct constructor will produce for BigRational. :(
    // To deal with it, we ignore "den" when "num" is 0.
    BigInteger num, den;  // invariant 1 <= den || (num == 0 && den == 0)
    public override string ToString() {
      int log10;
      if (num.IsZero || den.IsOne) {
        return string.Format("{0}.0", num);
      } else if (IsPowerOf10(den, out log10)) {
        string sign;
        string digits;
        if (num.Sign < 0) {
          sign = "-"; digits = (-num).ToString();
        } else {
          sign = ""; digits = num.ToString();
        }
        if (log10 < digits.Length) {
          var n = digits.Length - log10;
          return string.Format("{0}{1}.{2}", sign, digits.Substring(0, n), digits.Substring(n));
        } else {
          return string.Format("{0}0.{1}{2}", sign, new string('0', log10 - digits.Length), digits);
        }
      } else {
        return string.Format("({0}.0 / {1}.0)", num, den);
      }
    }
    public bool IsPowerOf10(BigInteger x, out int log10) {
      log10 = 0;
      if (x.IsZero) {
        return false;
      }
      while (true) {  // invariant: x != 0 && x * 10^log10 == old(x)
        if (x.IsOne) {
          return true;
        } else if (x % 10 == 0) {
          log10++;
          x /= 10;
        } else {
          return false;
        }
      }
    }
    public BigRational(int n) {
      num = new BigInteger(n);
      den = BigInteger.One;
    }
    public BigRational(BigInteger n, BigInteger d) {
      // requires 1 <= d
      num = n;
      den = d;
    }
    public BigInteger ToBigInteger() {
      if (num.IsZero || den.IsOne) {
        return num;
      } else if (0 < num.Sign) {
        return num / den;
      } else {
        return (num - den + 1) / den;
      }
    }
    /// <summary>
    /// Returns values such that aa/dd == a and bb/dd == b.
    /// </summary>
    private static void Normalize(BigRational a, BigRational b, out BigInteger aa, out BigInteger bb, out BigInteger dd) {
      if (a.num.IsZero) {
        aa = a.num;
        bb = b.num;
        dd = b.den;
      } else if (b.num.IsZero) {
        aa = a.num;
        dd = a.den;
        bb = b.num;
      } else {
        var gcd = BigInteger.GreatestCommonDivisor(a.den, b.den);
        var xx = a.den / gcd;
        var yy = b.den / gcd;
        // We now have a == a.num / (xx * gcd) and b == b.num / (yy * gcd).
        aa = a.num * yy;
        bb = b.num * xx;
        dd = a.den * yy;
      }
    }
    public int CompareTo(BigRational that) {
      // simple things first
      int asign = this.num.Sign;
      int bsign = that.num.Sign;
      if (asign < 0 && 0 <= bsign) {
        return -1;
      } else if (asign <= 0 && 0 < bsign) {
        return -1;
      } else if (bsign < 0 && 0 <= asign) {
        return 1;
      } else if (bsign <= 0 && 0 < asign) {
        return 1;
      }
      BigInteger aa, bb, dd;
      Normalize(this, that, out aa, out bb, out dd);
      return aa.CompareTo(bb);
    }
    public int Sign {
      get {
        return num.Sign;
      }
    }
    public override int GetHashCode() {
      return num.GetHashCode() + 29 * den.GetHashCode();
    }
    public override bool Equals(object obj) {
      if (obj is BigRational) {
        return this == (BigRational)obj;
      } else {
        return false;
      }
    }
    public static bool operator ==(BigRational a, BigRational b) {
      return a.CompareTo(b) == 0;
    }
    public static bool operator !=(BigRational a, BigRational b) {
      return a.CompareTo(b) != 0;
    }
    public static bool operator >(BigRational a, BigRational b) {
      return a.CompareTo(b) > 0;
    }
    public static bool operator >=(BigRational a, BigRational b) {
      return a.CompareTo(b) >= 0;
    }
    public static bool operator <(BigRational a, BigRational b) {
      return a.CompareTo(b) < 0;
    }
    public static bool operator <=(BigRational a, BigRational b) {
      return a.CompareTo(b) <= 0;
    }
    public static BigRational operator +(BigRational a, BigRational b) {
      BigInteger aa, bb, dd;
      Normalize(a, b, out aa, out bb, out dd);
      return new BigRational(aa + bb, dd);
    }
    public static BigRational operator -(BigRational a, BigRational b) {
      BigInteger aa, bb, dd;
      Normalize(a, b, out aa, out bb, out dd);
      return new BigRational(aa - bb, dd);
    }
    public static BigRational operator -(BigRational a) {
      return new BigRational(-a.num, a.den);
    }
    public static BigRational operator *(BigRational a, BigRational b) {
      return new BigRational(a.num * b.num, a.den * b.den);
    }
    public static BigRational operator /(BigRational a, BigRational b) {
      // Compute the reciprocal of b
      BigRational bReciprocal;
      if (0 < b.num.Sign) {
        bReciprocal = new BigRational(b.den, b.num);
      } else {
        // this is the case b.num < 0
        bReciprocal = new BigRational(-b.den, -b.num);
      }
      return a * bReciprocal;
    }
  }

  public class HaltException : Exception {
    public HaltException(object message) : base(message.ToString()) {
    }
  }
}

namespace @_System {
  public interface _ITuple2<out T0, out T1> {
    T0 dtor__0 { get; }
    T1 dtor__1 { get; }
  }

  public class Tuple2<T0, T1> : _ITuple2<T0, T1> {
    public readonly T0 _0;
    public readonly T1 _1;
    public Tuple2(T0 _0, T1 _1) {
      this._0 = _0;
      this._1 = _1;
    }
    public override bool Equals(object other) {
      var oth = other as _System.Tuple2<T0, T1>;
      return oth != null && object.Equals(this._0, oth._0) && object.Equals(this._1, oth._1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._1));
      return (int)hash;
    }
    public override string ToString() {
      string s = "";
      s += "(";
      s += Dafny.Helpers.ToString(this._0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._1);
      s += ")";
      return s;
    }
    public static _ITuple2<T0, T1> Default(T0 _default_T0, T1 _default_T1) {
      return create(_default_T0, _default_T1);
    }
    public static Dafny.TypeDescriptor<_System._ITuple2<T0, T1>> _TypeDescriptor(Dafny.TypeDescriptor<T0> _td_T0, Dafny.TypeDescriptor<T1> _td_T1) {
      return new Dafny.TypeDescriptor<_System._ITuple2<T0, T1>>(_System.Tuple2<T0, T1>.Default(_td_T0.Default(), _td_T1.Default()));
    }
    public static _ITuple2<T0, T1> create(T0 _0, T1 _1) {
      return new Tuple2<T0, T1>(_0, _1);
    }
    public T0 dtor__0 {
      get {
        return this._0;
      }
    }
    public T1 dtor__1 {
      get {
        return this._1;
      }
    }
  }

} // end of namespace _System
namespace Dafny {
  internal class ArrayHelpers {
    public static T[] InitNewArray1<T>(T z, BigInteger size0) {
      int s0 = (int)size0;
      T[] a = new T[s0];
      for (int i0 = 0; i0 < s0; i0++) {
        a[i0] = z;
      }
      return a;
    }
  }
} // end of namespace Dafny
public static class FuncExtensions {
  public static Func<U, UResult> DowncastClone<T, TResult, U, UResult>(this Func<T, TResult> F, Func<U, T> ArgConv, Func<TResult, UResult> ResConv) {
    return arg => ResConv(F(ArgConv(arg)));
  }
  public static Func<UResult> DowncastClone<TResult, UResult>(this Func<TResult> F, Func<TResult, UResult> ResConv) {
    return () => ResConv(F());
  }
}
namespace _System {

  public partial class nat {
    private static readonly Dafny.TypeDescriptor<BigInteger> _TYPE = new Dafny.TypeDescriptor<BigInteger>(BigInteger.Zero);
    public static Dafny.TypeDescriptor<BigInteger> _TypeDescriptor() {
      return _TYPE;
    }
  }

  public interface _ITuple0 {
    _ITuple0 DowncastClone();
  }
  public class Tuple0 : _ITuple0 {
    public Tuple0() {
    }
    public _ITuple0 DowncastClone() {
      if (this is _ITuple0 dt) { return dt; }
      return new Tuple0();
    }
    public override bool Equals(object other) {
      var oth = other as _System.Tuple0;
      return oth != null;
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      return (int) hash;
    }
    public override string ToString() {
      return "()";
    }
    private static readonly _ITuple0 theDefault = create();
    public static _ITuple0 Default() {
      return theDefault;
    }
    private static readonly Dafny.TypeDescriptor<_System._ITuple0> _TYPE = new Dafny.TypeDescriptor<_System._ITuple0>(_System.Tuple0.Default());
    public static Dafny.TypeDescriptor<_System._ITuple0> _TypeDescriptor() {
      return _TYPE;
    }
    public static _ITuple0 create() {
      return new Tuple0();
    }
    public static System.Collections.Generic.IEnumerable<_ITuple0> AllSingletonConstructors {
      get {
        yield return Tuple0.create();
      }
    }
  }
} // end of namespace _System
namespace _module {

  public interface _ICom5 {
    bool is_Print { get; }
    bool is_IsAsk { get; }
    bool is_Assign { get; }
    bool is_Turn { get; }
    bool is_Forward { get; }
    bool is_Sleep { get; }
    bool is_AddTo { get; }
    bool is_RemoveFrom { get; }
    bool is_If { get; }
    bool is_IfElse { get; }
    bool is_Seq { get; }
    Dafny.ISequence<char> dtor_Print_a0 { get; }
    Dafny.ISequence<char> dtor_IsAsk_a0 { get; }
    Dafny.ISequence<char> dtor_IsAsk_a1 { get; }
    Dafny.ISequence<char> dtor_Assign_a0 { get; }
    _IM dtor_Assign_a1 { get; }
    _IO5 dtor_Turn_a0 { get; }
    _IO5 dtor_Forward_a0 { get; }
    _IO5 dtor_Sleep_a0 { get; }
    _IM dtor_AddTo_a0 { get; }
    Dafny.ISequence<_IM> dtor_AddTo_a1 { get; }
    _IM dtor_RemoveFrom_a0 { get; }
    Dafny.ISequence<_IM> dtor_RemoveFrom_a1 { get; }
    _IB dtor_If_a0 { get; }
    _ICom5 dtor_If_a1 { get; }
    _IB dtor_IfElse_a0 { get; }
    _ICom5 dtor_IfElse_a1 { get; }
    _ICom5 dtor_IfElse_a2 { get; }
    _ICom5 dtor_Seq_a0 { get; }
    _ICom5 dtor_Seq_a1 { get; }
    _ICom5 DowncastClone();
  }
  public abstract class Com5 : _ICom5 {
    public Com5() { }
    private static readonly _ICom5 theDefault = create_Print(Dafny.Sequence<char>.Empty);
    public static _ICom5 Default() {
      return theDefault;
    }
    private static readonly Dafny.TypeDescriptor<_ICom5> _TYPE = new Dafny.TypeDescriptor<_ICom5>(Com5.Default());
    public static Dafny.TypeDescriptor<_ICom5> _TypeDescriptor() {
      return _TYPE;
    }
    public static _ICom5 create_Print(Dafny.ISequence<char> _a0) {
      return new Com5_Print(_a0);
    }
    public static _ICom5 create_IsAsk(Dafny.ISequence<char> _a0, Dafny.ISequence<char> _a1) {
      return new Com5_IsAsk(_a0, _a1);
    }
    public static _ICom5 create_Assign(Dafny.ISequence<char> _a0, _IM _a1) {
      return new Com5_Assign(_a0, _a1);
    }
    public static _ICom5 create_Turn(_IO5 _a0) {
      return new Com5_Turn(_a0);
    }
    public static _ICom5 create_Forward(_IO5 _a0) {
      return new Com5_Forward(_a0);
    }
    public static _ICom5 create_Sleep(_IO5 _a0) {
      return new Com5_Sleep(_a0);
    }
    public static _ICom5 create_AddTo(_IM _a0, Dafny.ISequence<_IM> _a1) {
      return new Com5_AddTo(_a0, _a1);
    }
    public static _ICom5 create_RemoveFrom(_IM _a0, Dafny.ISequence<_IM> _a1) {
      return new Com5_RemoveFrom(_a0, _a1);
    }
    public static _ICom5 create_If(_IB _a0, _ICom5 _a1) {
      return new Com5_If(_a0, _a1);
    }
    public static _ICom5 create_IfElse(_IB _a0, _ICom5 _a1, _ICom5 _a2) {
      return new Com5_IfElse(_a0, _a1, _a2);
    }
    public static _ICom5 create_Seq(_ICom5 _a0, _ICom5 _a1) {
      return new Com5_Seq(_a0, _a1);
    }
    public bool is_Print { get { return this is Com5_Print; } }
    public bool is_IsAsk { get { return this is Com5_IsAsk; } }
    public bool is_Assign { get { return this is Com5_Assign; } }
    public bool is_Turn { get { return this is Com5_Turn; } }
    public bool is_Forward { get { return this is Com5_Forward; } }
    public bool is_Sleep { get { return this is Com5_Sleep; } }
    public bool is_AddTo { get { return this is Com5_AddTo; } }
    public bool is_RemoveFrom { get { return this is Com5_RemoveFrom; } }
    public bool is_If { get { return this is Com5_If; } }
    public bool is_IfElse { get { return this is Com5_IfElse; } }
    public bool is_Seq { get { return this is Com5_Seq; } }
    public Dafny.ISequence<char> dtor_Print_a0 {
      get {
        var d = this;
        return ((Com5_Print)d)._a0;
      }
    }
    public Dafny.ISequence<char> dtor_IsAsk_a0 {
      get {
        var d = this;
        return ((Com5_IsAsk)d)._a0;
      }
    }
    public Dafny.ISequence<char> dtor_IsAsk_a1 {
      get {
        var d = this;
        return ((Com5_IsAsk)d)._a1;
      }
    }
    public Dafny.ISequence<char> dtor_Assign_a0 {
      get {
        var d = this;
        return ((Com5_Assign)d)._a0;
      }
    }
    public _IM dtor_Assign_a1 {
      get {
        var d = this;
        return ((Com5_Assign)d)._a1;
      }
    }
    public _IO5 dtor_Turn_a0 {
      get {
        var d = this;
        return ((Com5_Turn)d)._a0;
      }
    }
    public _IO5 dtor_Forward_a0 {
      get {
        var d = this;
        return ((Com5_Forward)d)._a0;
      }
    }
    public _IO5 dtor_Sleep_a0 {
      get {
        var d = this;
        return ((Com5_Sleep)d)._a0;
      }
    }
    public _IM dtor_AddTo_a0 {
      get {
        var d = this;
        return ((Com5_AddTo)d)._a0;
      }
    }
    public Dafny.ISequence<_IM> dtor_AddTo_a1 {
      get {
        var d = this;
        return ((Com5_AddTo)d)._a1;
      }
    }
    public _IM dtor_RemoveFrom_a0 {
      get {
        var d = this;
        return ((Com5_RemoveFrom)d)._a0;
      }
    }
    public Dafny.ISequence<_IM> dtor_RemoveFrom_a1 {
      get {
        var d = this;
        return ((Com5_RemoveFrom)d)._a1;
      }
    }
    public _IB dtor_If_a0 {
      get {
        var d = this;
        return ((Com5_If)d)._a0;
      }
    }
    public _ICom5 dtor_If_a1 {
      get {
        var d = this;
        return ((Com5_If)d)._a1;
      }
    }
    public _IB dtor_IfElse_a0 {
      get {
        var d = this;
        return ((Com5_IfElse)d)._a0;
      }
    }
    public _ICom5 dtor_IfElse_a1 {
      get {
        var d = this;
        return ((Com5_IfElse)d)._a1;
      }
    }
    public _ICom5 dtor_IfElse_a2 {
      get {
        var d = this;
        return ((Com5_IfElse)d)._a2;
      }
    }
    public _ICom5 dtor_Seq_a0 {
      get {
        var d = this;
        return ((Com5_Seq)d)._a0;
      }
    }
    public _ICom5 dtor_Seq_a1 {
      get {
        var d = this;
        return ((Com5_Seq)d)._a1;
      }
    }
    public abstract _ICom5 DowncastClone();
  }
  public class Com5_Print : Com5 {
    public readonly Dafny.ISequence<char> _a0;
    public Com5_Print(Dafny.ISequence<char> _a0) {
      this._a0 = _a0;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_Print(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_Print;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.Print";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class Com5_IsAsk : Com5 {
    public readonly Dafny.ISequence<char> _a0;
    public readonly Dafny.ISequence<char> _a1;
    public Com5_IsAsk(Dafny.ISequence<char> _a0, Dafny.ISequence<char> _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_IsAsk(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_IsAsk;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 1;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.IsAsk";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }
  public class Com5_Assign : Com5 {
    public readonly Dafny.ISequence<char> _a0;
    public readonly _IM _a1;
    public Com5_Assign(Dafny.ISequence<char> _a0, _IM _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_Assign(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_Assign;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 2;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.Assign";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }
  public class Com5_Turn : Com5 {
    public readonly _IO5 _a0;
    public Com5_Turn(_IO5 _a0) {
      this._a0 = _a0;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_Turn(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_Turn;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 3;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.Turn";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class Com5_Forward : Com5 {
    public readonly _IO5 _a0;
    public Com5_Forward(_IO5 _a0) {
      this._a0 = _a0;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_Forward(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_Forward;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 4;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.Forward";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class Com5_Sleep : Com5 {
    public readonly _IO5 _a0;
    public Com5_Sleep(_IO5 _a0) {
      this._a0 = _a0;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_Sleep(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_Sleep;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 5;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.Sleep";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class Com5_AddTo : Com5 {
    public readonly _IM _a0;
    public readonly Dafny.ISequence<_IM> _a1;
    public Com5_AddTo(_IM _a0, Dafny.ISequence<_IM> _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_AddTo(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_AddTo;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 6;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.AddTo";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }
  public class Com5_RemoveFrom : Com5 {
    public readonly _IM _a0;
    public readonly Dafny.ISequence<_IM> _a1;
    public Com5_RemoveFrom(_IM _a0, Dafny.ISequence<_IM> _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_RemoveFrom(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_RemoveFrom;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 7;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.RemoveFrom";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }
  public class Com5_If : Com5 {
    public readonly _IB _a0;
    public readonly _ICom5 _a1;
    public Com5_If(_IB _a0, _ICom5 _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_If(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_If;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 8;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.If";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }
  public class Com5_IfElse : Com5 {
    public readonly _IB _a0;
    public readonly _ICom5 _a1;
    public readonly _ICom5 _a2;
    public Com5_IfElse(_IB _a0, _ICom5 _a1, _ICom5 _a2) {
      this._a0 = _a0;
      this._a1 = _a1;
      this._a2 = _a2;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_IfElse(_a0, _a1, _a2);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_IfElse;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1) && object.Equals(this._a2, oth._a2);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 9;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a2));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.IfElse";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a2);
      s += ")";
      return s;
    }
  }
  public class Com5_Seq : Com5 {
    public readonly _ICom5 _a0;
    public readonly _ICom5 _a1;
    public Com5_Seq(_ICom5 _a0, _ICom5 _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _ICom5 DowncastClone() {
      if (this is _ICom5 dt) { return dt; }
      return new Com5_Seq(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as Com5_Seq;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 10;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Com5.Seq";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }

  public interface _IO5 {
    bool is_Empty { get; }
    bool is_N { get; }
    bool is_V { get; }
    bool is_AtRandom { get; }
    BigInteger dtor_N_a0 { get; }
    Dafny.ISequence<char> dtor_V_a0 { get; }
    Dafny.ISequence<_IM> dtor_AtRandom_a0 { get; }
    _IO5 DowncastClone();
  }
  public abstract class O5 : _IO5 {
    public O5() { }
    private static readonly _IO5 theDefault = create_Empty();
    public static _IO5 Default() {
      return theDefault;
    }
    private static readonly Dafny.TypeDescriptor<_IO5> _TYPE = new Dafny.TypeDescriptor<_IO5>(O5.Default());
    public static Dafny.TypeDescriptor<_IO5> _TypeDescriptor() {
      return _TYPE;
    }
    public static _IO5 create_Empty() {
      return new O5_Empty();
    }
    public static _IO5 create_N(BigInteger _a0) {
      return new O5_N(_a0);
    }
    public static _IO5 create_V(Dafny.ISequence<char> _a0) {
      return new O5_V(_a0);
    }
    public static _IO5 create_AtRandom(Dafny.ISequence<_IM> _a0) {
      return new O5_AtRandom(_a0);
    }
    public bool is_Empty { get { return this is O5_Empty; } }
    public bool is_N { get { return this is O5_N; } }
    public bool is_V { get { return this is O5_V; } }
    public bool is_AtRandom { get { return this is O5_AtRandom; } }
    public BigInteger dtor_N_a0 {
      get {
        var d = this;
        return ((O5_N)d)._a0;
      }
    }
    public Dafny.ISequence<char> dtor_V_a0 {
      get {
        var d = this;
        return ((O5_V)d)._a0;
      }
    }
    public Dafny.ISequence<_IM> dtor_AtRandom_a0 {
      get {
        var d = this;
        return ((O5_AtRandom)d)._a0;
      }
    }
    public abstract _IO5 DowncastClone();
  }
  public class O5_Empty : O5 {
    public O5_Empty() {
    }
    public override _IO5 DowncastClone() {
      if (this is _IO5 dt) { return dt; }
      return new O5_Empty();
    }
    public override bool Equals(object other) {
      var oth = other as O5_Empty;
      return oth != null;
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      return (int) hash;
    }
    public override string ToString() {
      string s = "O5.Empty";
      return s;
    }
  }
  public class O5_N : O5 {
    public readonly BigInteger _a0;
    public O5_N(BigInteger _a0) {
      this._a0 = _a0;
    }
    public override _IO5 DowncastClone() {
      if (this is _IO5 dt) { return dt; }
      return new O5_N(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as O5_N;
      return oth != null && this._a0 == oth._a0;
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 1;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "O5.N";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class O5_V : O5 {
    public readonly Dafny.ISequence<char> _a0;
    public O5_V(Dafny.ISequence<char> _a0) {
      this._a0 = _a0;
    }
    public override _IO5 DowncastClone() {
      if (this is _IO5 dt) { return dt; }
      return new O5_V(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as O5_V;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 2;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "O5.V";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class O5_AtRandom : O5 {
    public readonly Dafny.ISequence<_IM> _a0;
    public O5_AtRandom(Dafny.ISequence<_IM> _a0) {
      this._a0 = _a0;
    }
    public override _IO5 DowncastClone() {
      if (this is _IO5 dt) { return dt; }
      return new O5_AtRandom(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as O5_AtRandom;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 3;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "O5.AtRandom";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }

  public interface _IM {
    bool is_N { get; }
    bool is_V { get; }
    bool is_L { get; }
    BigInteger dtor_N_a0 { get; }
    Dafny.ISequence<char> dtor_V_a0 { get; }
    Dafny.ISequence<_IM> dtor_L_a0 { get; }
    _IM DowncastClone();
  }
  public abstract class M : _IM {
    public M() { }
    private static readonly _IM theDefault = create_N(BigInteger.Zero);
    public static _IM Default() {
      return theDefault;
    }
    private static readonly Dafny.TypeDescriptor<_IM> _TYPE = new Dafny.TypeDescriptor<_IM>(M.Default());
    public static Dafny.TypeDescriptor<_IM> _TypeDescriptor() {
      return _TYPE;
    }
    public static _IM create_N(BigInteger _a0) {
      return new M_N(_a0);
    }
    public static _IM create_V(Dafny.ISequence<char> _a0) {
      return new M_V(_a0);
    }
    public static _IM create_L(Dafny.ISequence<_IM> _a0) {
      return new M_L(_a0);
    }
    public bool is_N { get { return this is M_N; } }
    public bool is_V { get { return this is M_V; } }
    public bool is_L { get { return this is M_L; } }
    public BigInteger dtor_N_a0 {
      get {
        var d = this;
        return ((M_N)d)._a0;
      }
    }
    public Dafny.ISequence<char> dtor_V_a0 {
      get {
        var d = this;
        return ((M_V)d)._a0;
      }
    }
    public Dafny.ISequence<_IM> dtor_L_a0 {
      get {
        var d = this;
        return ((M_L)d)._a0;
      }
    }
    public abstract _IM DowncastClone();
  }
  public class M_N : M {
    public readonly BigInteger _a0;
    public M_N(BigInteger _a0) {
      this._a0 = _a0;
    }
    public override _IM DowncastClone() {
      if (this is _IM dt) { return dt; }
      return new M_N(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as M_N;
      return oth != null && this._a0 == oth._a0;
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "M.N";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class M_V : M {
    public readonly Dafny.ISequence<char> _a0;
    public M_V(Dafny.ISequence<char> _a0) {
      this._a0 = _a0;
    }
    public override _IM DowncastClone() {
      if (this is _IM dt) { return dt; }
      return new M_V(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as M_V;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 1;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "M.V";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }
  public class M_L : M {
    public readonly Dafny.ISequence<_IM> _a0;
    public M_L(Dafny.ISequence<_IM> _a0) {
      this._a0 = _a0;
    }
    public override _IM DowncastClone() {
      if (this is _IM dt) { return dt; }
      return new M_L(_a0);
    }
    public override bool Equals(object other) {
      var oth = other as M_L;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 2;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "M.L";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }

  public interface _IB {
    bool is_Eq { get; }
    bool is_Elem { get; }
    _IM dtor_Eq_a0 { get; }
    _IM dtor_Eq_a1 { get; }
    _IM dtor_Elem_a0 { get; }
    Dafny.ISequence<_IM> dtor_Elem_a1 { get; }
    _IB DowncastClone();
  }
  public abstract class B : _IB {
    public B() { }
    private static readonly _IB theDefault = create_Eq(M.Default(), M.Default());
    public static _IB Default() {
      return theDefault;
    }
    private static readonly Dafny.TypeDescriptor<_IB> _TYPE = new Dafny.TypeDescriptor<_IB>(B.Default());
    public static Dafny.TypeDescriptor<_IB> _TypeDescriptor() {
      return _TYPE;
    }
    public static _IB create_Eq(_IM _a0, _IM _a1) {
      return new B_Eq(_a0, _a1);
    }
    public static _IB create_Elem(_IM _a0, Dafny.ISequence<_IM> _a1) {
      return new B_Elem(_a0, _a1);
    }
    public bool is_Eq { get { return this is B_Eq; } }
    public bool is_Elem { get { return this is B_Elem; } }
    public _IM dtor_Eq_a0 {
      get {
        var d = this;
        return ((B_Eq)d)._a0;
      }
    }
    public _IM dtor_Eq_a1 {
      get {
        var d = this;
        return ((B_Eq)d)._a1;
      }
    }
    public _IM dtor_Elem_a0 {
      get {
        var d = this;
        return ((B_Elem)d)._a0;
      }
    }
    public Dafny.ISequence<_IM> dtor_Elem_a1 {
      get {
        var d = this;
        return ((B_Elem)d)._a1;
      }
    }
    public abstract _IB DowncastClone();
  }
  public class B_Eq : B {
    public readonly _IM _a0;
    public readonly _IM _a1;
    public B_Eq(_IM _a0, _IM _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _IB DowncastClone() {
      if (this is _IB dt) { return dt; }
      return new B_Eq(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as B_Eq;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "B.Eq";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }
  public class B_Elem : B {
    public readonly _IM _a0;
    public readonly Dafny.ISequence<_IM> _a1;
    public B_Elem(_IM _a0, Dafny.ISequence<_IM> _a1) {
      this._a0 = _a0;
      this._a1 = _a1;
    }
    public override _IB DowncastClone() {
      if (this is _IB dt) { return dt; }
      return new B_Elem(_a0, _a1);
    }
    public override bool Equals(object other) {
      var oth = other as B_Elem;
      return oth != null && object.Equals(this._a0, oth._a0) && object.Equals(this._a1, oth._a1);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 1;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a1));
      return (int) hash;
    }
    public override string ToString() {
      string s = "B.Elem";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ", ";
      s += Dafny.Helpers.ToString(this._a1);
      s += ")";
      return s;
    }
  }

  public interface Env5 {
    bool turtle__exists { get; set; }
    Dafny.IMap<Dafny.ISequence<char>,_IM> sigma { get; set; }
    void Print(Dafny.ISequence<char> output);
    _IM Ask(Dafny.ISequence<char> question);
    void Turn(BigInteger angle);
    void Forward(BigInteger step);
    void Draw();
    void Assign(Dafny.ISequence<char> variable, _IM @value);
    void Sleep(BigInteger time);
    Dafny.ISequence<char> SubstText(Dafny.ISequence<char> plaintext);
    BigInteger SubstNumber(Dafny.ISequence<char> name);
    void Error(Dafny.ISequence<char> exception);
    void AddTo(_IM element, Dafny.ISequence<_IM> list);
    void RemoveFrom(_IM element, Dafny.ISequence<_IM> list);
    _IM Random(Dafny.ISequence<_IM> list);
    bool Eq(_IM x, _IM y);
    bool Elem(_IM x, Dafny.ISequence<_IM> y);
  }
  public class _Companion_Env5 {
    public static void Assign(Env5 _this, Dafny.ISequence<char> variable, _IM @value)
    {
      (_this).sigma = Dafny.Map<Dafny.ISequence<char>, _IM>.Update(_this.sigma, variable, @value);
    }
    public static Dafny.ISequence<char> SubstText(Env5 _this, Dafny.ISequence<char> plaintext)
    {
      Dafny.ISequence<char> valuestext = Dafny.Sequence<char>.Empty;
      BigInteger _283_indexbegin;
      _283_indexbegin = (new BigInteger((plaintext).Count)) + (BigInteger.One);
      BigInteger _284_indexend;
      _284_indexend = (new BigInteger((plaintext).Count)) + (BigInteger.One);
      bool _285_quotes;
      _285_quotes = false;
      BigInteger _hi0 = new BigInteger((plaintext).Count);
      for (BigInteger _286_i = BigInteger.Zero; _286_i < _hi0; _286_i++) {
        if (((plaintext).Select(_286_i)) == ('\'')) {
          _285_quotes = !(_285_quotes);
        }
        BigInteger _hi1 = new BigInteger((plaintext).Count);
        for (BigInteger _287_j = _286_i; _287_j < _hi1; _287_j++) {
          if (((_this.sigma).Contains(((plaintext).Subsequence(_286_i, _287_j)))) && (!(_285_quotes))) {
            _283_indexbegin = _286_i;
            _284_indexend = _287_j;
            _IM _source0 = Dafny.Map<Dafny.ISequence<char>, _IM>.Select(_this.sigma,(plaintext).Subsequence(_286_i, _287_j));
            if (_source0.is_N) {
              BigInteger _288___mcc_h0 = _source0.dtor_N_a0;
              BigInteger _289_x = _288___mcc_h0;
              (_this).Error(Dafny.Sequence<char>.FromString("Text used without quotes"));
            } else if (_source0.is_V) {
              Dafny.ISequence<char> _290___mcc_h1 = _source0.dtor_V_a0;
              Dafny.ISequence<char> _291_x = _290___mcc_h1;
              valuestext = Dafny.Sequence<char>.Concat(valuestext, _291_x);
            } else {
              Dafny.ISequence<_IM> _292___mcc_h2 = _source0.dtor_L_a0;
              Dafny.ISequence<_IM> _293_x = _292___mcc_h2;
              (_this).Error(Dafny.Sequence<char>.FromString("Cannot print a list"));
            }
          }
        }
        if ((((_286_i) < (_283_indexbegin)) || ((_286_i) > (_284_indexend))) && (((plaintext).Select(_286_i)) != ('\''))) {
          valuestext = Dafny.Sequence<char>.Concat(valuestext, Dafny.Sequence<char>.FromElements((plaintext).Select(_286_i)));
        }
      }
      return valuestext;
    }
    public static BigInteger SubstNumber(Env5 _this, Dafny.ISequence<char> name)
    {
      BigInteger number = BigInteger.Zero;
      if ((_this.sigma).Contains((name))) {
        _IM _source1 = Dafny.Map<Dafny.ISequence<char>, _IM>.Select(_this.sigma,name);
        if (_source1.is_N) {
          BigInteger _294___mcc_h0 = _source1.dtor_N_a0;
          BigInteger _295_x = _294___mcc_h0;
          number = _295_x;
        } else if (_source1.is_V) {
          Dafny.ISequence<char> _296___mcc_h1 = _source1.dtor_V_a0;
          Dafny.ISequence<char> _297_x = _296___mcc_h1;
          (_this).Error(Dafny.Sequence<char>.FromString("the value of this variable is not a number but a string"));
        } else {
          Dafny.ISequence<_IM> _298___mcc_h2 = _source1.dtor_L_a0;
          Dafny.ISequence<_IM> _299_x = _298___mcc_h2;
          (_this).Error(Dafny.Sequence<char>.FromString("the value of this variable is not a number but a list"));
        }
      } else {
        (_this).Error(Dafny.Sequence<char>.FromString("not a variable"));
      }
      return number;
    }
    public static bool Eq(Env5 _this, _IM x, _IM y)
    {
      bool cond = false;
      _System._ITuple2<_IM, _IM> _source2 = _System.Tuple2<_IM, _IM>.create(x, y);
      {
        _IM _300___mcc_h0 = _source2.dtor__0;
        _IM _301___mcc_h1 = _source2.dtor__1;
        _IM _source3 = _300___mcc_h0;
        if (_source3.is_N) {
          BigInteger _302___mcc_h2 = _source3.dtor_N_a0;
          _IM _source4 = _301___mcc_h1;
          if (_source4.is_N) {
            BigInteger _303___mcc_h3 = _source4.dtor_N_a0;
            BigInteger _304_n2 = _303___mcc_h3;
            BigInteger _305_n1 = _302___mcc_h2;
            cond = (_305_n1) == (_304_n2);
          } else if (_source4.is_V) {
            Dafny.ISequence<char> _306___mcc_h4 = _source4.dtor_V_a0;
            Dafny.ISequence<char> _307_v = _306___mcc_h4;
            BigInteger _308_n = _302___mcc_h2;
            BigInteger _309_temp;
            BigInteger _out0;
            _out0 = (_this).SubstNumber(_307_v);
            _309_temp = _out0;
            cond = (_308_n) == (_309_temp);
          } else {
            Dafny.ISequence<_IM> _310___mcc_h5 = _source4.dtor_L_a0;
            Dafny.ISequence<_IM> _311_l = _310___mcc_h5;
            BigInteger _312_n = _302___mcc_h2;
            (_this).Error(Dafny.Sequence<char>.FromString("Cannot compare list with int"));
          }
        } else if (_source3.is_V) {
          Dafny.ISequence<char> _313___mcc_h6 = _source3.dtor_V_a0;
          _IM _source5 = _301___mcc_h1;
          if (_source5.is_N) {
            BigInteger _314___mcc_h7 = _source5.dtor_N_a0;
            BigInteger _315_n = _314___mcc_h7;
            Dafny.ISequence<char> _316_v = _313___mcc_h6;
            BigInteger _317_temp;
            BigInteger _out1;
            _out1 = (_this).SubstNumber(_316_v);
            _317_temp = _out1;
            cond = (_315_n) == (_317_temp);
          } else if (_source5.is_V) {
            Dafny.ISequence<char> _318___mcc_h8 = _source5.dtor_V_a0;
            Dafny.ISequence<char> _319_v2 = _318___mcc_h8;
            Dafny.ISequence<char> _320_v1 = _313___mcc_h6;
            Dafny.ISequence<char> _321_temp1;
            Dafny.ISequence<char> _out2;
            _out2 = (_this).SubstText(_320_v1);
            _321_temp1 = _out2;
            Dafny.ISequence<char> _322_temp2;
            Dafny.ISequence<char> _out3;
            _out3 = (_this).SubstText(_319_v2);
            _322_temp2 = _out3;
            cond = (_321_temp1).Equals((_322_temp2));
          } else {
            Dafny.ISequence<_IM> _323___mcc_h9 = _source5.dtor_L_a0;
            Dafny.ISequence<_IM> _324_l = _323___mcc_h9;
            Dafny.ISequence<char> _325_v = _313___mcc_h6;
            (_this).Error(Dafny.Sequence<char>.FromString("Cannot compare variable or string with list"));
          }
        } else {
          Dafny.ISequence<_IM> _326___mcc_h10 = _source3.dtor_L_a0;
          _IM _source6 = _301___mcc_h1;
          if (_source6.is_N) {
            BigInteger _327___mcc_h11 = _source6.dtor_N_a0;
            BigInteger _328_n = _327___mcc_h11;
            Dafny.ISequence<_IM> _329_l = _326___mcc_h10;
            (_this).Error(Dafny.Sequence<char>.FromString("Cannot compare list with int"));
          } else if (_source6.is_V) {
            Dafny.ISequence<char> _330___mcc_h12 = _source6.dtor_V_a0;
            Dafny.ISequence<char> _331_v = _330___mcc_h12;
            Dafny.ISequence<_IM> _332_l = _326___mcc_h10;
            (_this).Error(Dafny.Sequence<char>.FromString("Cannot compare variable or string with list"));
          } else {
            Dafny.ISequence<_IM> _333___mcc_h13 = _source6.dtor_L_a0;
            Dafny.ISequence<_IM> _334_l2 = _333___mcc_h13;
            Dafny.ISequence<_IM> _335_l1 = _326___mcc_h10;
            cond = (_335_l1).Equals((_334_l2));
          }
        }
      }
      return cond;
    }
    public static bool Elem(Env5 _this, _IM x, Dafny.ISequence<_IM> y)
    {
      bool cond = false;
      cond = false;
      BigInteger _hi2 = new BigInteger((y).Count);
      for (BigInteger _336_i = BigInteger.Zero; _336_i < _hi2; _336_i++) {
        if ((object.Equals(x, (y).Select(_336_i))) && ((cond) == (false))) {
          cond = true;
        }
      }
      return cond;
    }
  }

  public interface _IMaybe<T> {
    bool is_Nothing { get; }
    bool is_Just { get; }
    T dtor_Just_a0 { get; }
    _IMaybe<__T> DowncastClone<__T>(Func<T, __T> converter0);
  }
  public abstract class Maybe<T> : _IMaybe<T> {
    public Maybe() { }
    public static _IMaybe<T> Default() {
      return create_Nothing();
    }
    public static Dafny.TypeDescriptor<_IMaybe<T>> _TypeDescriptor() {
      return new Dafny.TypeDescriptor<_IMaybe<T>>(Maybe<T>.Default());
    }
    public static _IMaybe<T> create_Nothing() {
      return new Maybe_Nothing<T>();
    }
    public static _IMaybe<T> create_Just(T _a0) {
      return new Maybe_Just<T>(_a0);
    }
    public bool is_Nothing { get { return this is Maybe_Nothing<T>; } }
    public bool is_Just { get { return this is Maybe_Just<T>; } }
    public T dtor_Just_a0 {
      get {
        var d = this;
        return ((Maybe_Just<T>)d)._a0;
      }
    }
    public abstract _IMaybe<__T> DowncastClone<__T>(Func<T, __T> converter0);
  }
  public class Maybe_Nothing<T> : Maybe<T> {
    public Maybe_Nothing() {
    }
    public override _IMaybe<__T> DowncastClone<__T>(Func<T, __T> converter0) {
      if (this is _IMaybe<__T> dt) { return dt; }
      return new Maybe_Nothing<__T>();
    }
    public override bool Equals(object other) {
      var oth = other as Maybe_Nothing<T>;
      return oth != null;
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 0;
      return (int) hash;
    }
    public override string ToString() {
      string s = "Maybe.Nothing";
      return s;
    }
  }
  public class Maybe_Just<T> : Maybe<T> {
    public readonly T _a0;
    public Maybe_Just(T _a0) {
      this._a0 = _a0;
    }
    public override _IMaybe<__T> DowncastClone<__T>(Func<T, __T> converter0) {
      if (this is _IMaybe<__T> dt) { return dt; }
      return new Maybe_Just<__T>(converter0(_a0));
    }
    public override bool Equals(object other) {
      var oth = other as Maybe_Just<T>;
      return oth != null && object.Equals(this._a0, oth._a0);
    }
    public override int GetHashCode() {
      ulong hash = 5381;
      hash = ((hash << 5) + hash) + 1;
      hash = ((hash << 5) + hash) + ((ulong)Dafny.Helpers.GetHashCode(this._a0));
      return (int) hash;
    }
    public override string ToString() {
      string s = "Maybe.Just";
      s += "(";
      s += Dafny.Helpers.ToString(this._a0);
      s += ")";
      return s;
    }
  }

  public partial class __default {
    public static void bigstep__level5(_ICom5 c, Env5 e)
    {
      _ICom5 _source7 = c;
      if (_source7.is_Print) {
        Dafny.ISequence<char> _337___mcc_h0 = _source7.dtor_Print_a0;
        Dafny.ISequence<char> _338_x = _337___mcc_h0;
        Dafny.ISequence<char> _339_temp;
        Dafny.ISequence<char> _out4;
        _out4 = (e).SubstText(_338_x);
        _339_temp = _out4;
        (e).Print(_339_temp);
      } else if (_source7.is_IsAsk) {
        Dafny.ISequence<char> _340___mcc_h1 = _source7.dtor_IsAsk_a0;
        Dafny.ISequence<char> _341___mcc_h2 = _source7.dtor_IsAsk_a1;
        Dafny.ISequence<char> _342_y = _341___mcc_h2;
        Dafny.ISequence<char> _343_x = _340___mcc_h1;
        _IM _344_answer;
        _IM _out5;
        _out5 = (e).Ask(_342_y);
        _344_answer = _out5;
        (e).Assign(_343_x, _344_answer);
      } else if (_source7.is_Assign) {
        Dafny.ISequence<char> _345___mcc_h3 = _source7.dtor_Assign_a0;
        _IM _346___mcc_h4 = _source7.dtor_Assign_a1;
        _IM _347_y = _346___mcc_h4;
        Dafny.ISequence<char> _348_x = _345___mcc_h3;
        (e).Assign(_348_x, _347_y);
      } else if (_source7.is_Turn) {
        _IO5 _349___mcc_h5 = _source7.dtor_Turn_a0;
        _IO5 _350_x = _349___mcc_h5;
        BigInteger _351_num = BigInteger.Zero;
        _IO5 _source8 = _350_x;
        if (_source8.is_Empty) {
          _351_num = new BigInteger(-90);
        } else if (_source8.is_N) {
          BigInteger _352___mcc_h19 = _source8.dtor_N_a0;
          BigInteger _353_n = _352___mcc_h19;
          _351_num = _353_n;
        } else if (_source8.is_V) {
          Dafny.ISequence<char> _354___mcc_h20 = _source8.dtor_V_a0;
          Dafny.ISequence<char> _355_n = _354___mcc_h20;
          BigInteger _out6;
          _out6 = (e).SubstNumber(_355_n);
          _351_num = _out6;
        } else {
          Dafny.ISequence<_IM> _356___mcc_h21 = _source8.dtor_AtRandom_a0;
          Dafny.ISequence<_IM> _357_l = _356___mcc_h21;
          {
            _IM _358_temp;
            _IM _out7;
            _out7 = (e).Random(_357_l);
            _358_temp = _out7;
            _IM _source9 = _358_temp;
            if (_source9.is_N) {
              BigInteger _359___mcc_h22 = _source9.dtor_N_a0;
              BigInteger _360_m = _359___mcc_h22;
              _351_num = _360_m;
            } else if (_source9.is_V) {
              Dafny.ISequence<char> _361___mcc_h23 = _source9.dtor_V_a0;
              Dafny.ISequence<char> _362_m = _361___mcc_h23;
              (e).Error(Dafny.Sequence<char>.FromString("Using variables through a list and at random is not accepted"));
            } else {
              Dafny.ISequence<_IM> _363___mcc_h24 = _source9.dtor_L_a0;
              Dafny.ISequence<_IM> _364_m = _363___mcc_h24;
              (e).Error(Dafny.Sequence<char>.FromString("Nesting lists, so using lists of lists is not accepted"));
            }
          }
        }
        if ((e.turtle__exists) == (false)) {
          (e).Draw();
          (e).turtle__exists = true;
        }
        (e).Turn(_351_num);
      } else if (_source7.is_Forward) {
        _IO5 _365___mcc_h6 = _source7.dtor_Forward_a0;
        _IO5 _366_x = _365___mcc_h6;
        BigInteger _367_num = BigInteger.Zero;
        _IO5 _source10 = _366_x;
        if (_source10.is_Empty) {
          _367_num = new BigInteger(50);
        } else if (_source10.is_N) {
          BigInteger _368___mcc_h25 = _source10.dtor_N_a0;
          BigInteger _369_n = _368___mcc_h25;
          _367_num = _369_n;
        } else if (_source10.is_V) {
          Dafny.ISequence<char> _370___mcc_h26 = _source10.dtor_V_a0;
          Dafny.ISequence<char> _371_n = _370___mcc_h26;
          BigInteger _out8;
          _out8 = (e).SubstNumber(_371_n);
          _367_num = _out8;
        } else {
          Dafny.ISequence<_IM> _372___mcc_h27 = _source10.dtor_AtRandom_a0;
          Dafny.ISequence<_IM> _373_l = _372___mcc_h27;
          {
            _IM _374_temp;
            _IM _out9;
            _out9 = (e).Random(_373_l);
            _374_temp = _out9;
            _IM _source11 = _374_temp;
            if (_source11.is_N) {
              BigInteger _375___mcc_h28 = _source11.dtor_N_a0;
              BigInteger _376_m = _375___mcc_h28;
              _367_num = _376_m;
            } else if (_source11.is_V) {
              Dafny.ISequence<char> _377___mcc_h29 = _source11.dtor_V_a0;
              Dafny.ISequence<char> _378_m = _377___mcc_h29;
              (e).Error(Dafny.Sequence<char>.FromString("Using variables through a list and at random is not accepted"));
            } else {
              Dafny.ISequence<_IM> _379___mcc_h30 = _source11.dtor_L_a0;
              Dafny.ISequence<_IM> _380_m = _379___mcc_h30;
              (e).Error(Dafny.Sequence<char>.FromString("Nesting lists, so using lists of lists is not accepted"));
            }
          }
        }
        if ((e.turtle__exists) == (false)) {
          (e).Draw();
          (e).turtle__exists = true;
        }
        (e).Forward(_367_num);
      } else if (_source7.is_Sleep) {
        _IO5 _381___mcc_h7 = _source7.dtor_Sleep_a0;
        _IO5 _382_x = _381___mcc_h7;
        BigInteger _383_num = BigInteger.Zero;
        _IO5 _source12 = _382_x;
        if (_source12.is_Empty) {
          _383_num = BigInteger.One;
        } else if (_source12.is_N) {
          BigInteger _384___mcc_h31 = _source12.dtor_N_a0;
          BigInteger _385_n = _384___mcc_h31;
          _383_num = _385_n;
        } else if (_source12.is_V) {
          Dafny.ISequence<char> _386___mcc_h32 = _source12.dtor_V_a0;
          Dafny.ISequence<char> _387_n = _386___mcc_h32;
          BigInteger _out10;
          _out10 = (e).SubstNumber(_387_n);
          _383_num = _out10;
        } else {
          Dafny.ISequence<_IM> _388___mcc_h33 = _source12.dtor_AtRandom_a0;
          Dafny.ISequence<_IM> _389_l = _388___mcc_h33;
          {
            _IM _390_temp;
            _IM _out11;
            _out11 = (e).Random(_389_l);
            _390_temp = _out11;
            _IM _source13 = _390_temp;
            if (_source13.is_N) {
              BigInteger _391___mcc_h34 = _source13.dtor_N_a0;
              BigInteger _392_m = _391___mcc_h34;
              _383_num = _392_m;
            } else if (_source13.is_V) {
              Dafny.ISequence<char> _393___mcc_h35 = _source13.dtor_V_a0;
              Dafny.ISequence<char> _394_m = _393___mcc_h35;
              (e).Error(Dafny.Sequence<char>.FromString("Using variables through a list and at random is not accepted"));
            } else {
              Dafny.ISequence<_IM> _395___mcc_h36 = _source13.dtor_L_a0;
              Dafny.ISequence<_IM> _396_m = _395___mcc_h36;
              (e).Error(Dafny.Sequence<char>.FromString("Nesting lists, so using lists of lists is not accepted"));
            }
          }
        }
        (e).Sleep(_383_num);
      } else if (_source7.is_AddTo) {
        _IM _397___mcc_h8 = _source7.dtor_AddTo_a0;
        Dafny.ISequence<_IM> _398___mcc_h9 = _source7.dtor_AddTo_a1;
        Dafny.ISequence<_IM> _399_l = _398___mcc_h9;
        _IM _400_x = _397___mcc_h8;
        (e).AddTo(_400_x, _399_l);
      } else if (_source7.is_RemoveFrom) {
        _IM _401___mcc_h10 = _source7.dtor_RemoveFrom_a0;
        Dafny.ISequence<_IM> _402___mcc_h11 = _source7.dtor_RemoveFrom_a1;
        Dafny.ISequence<_IM> _403_l = _402___mcc_h11;
        _IM _404_x = _401___mcc_h10;
        (e).RemoveFrom(_404_x, _403_l);
      } else if (_source7.is_If) {
        _IB _405___mcc_h12 = _source7.dtor_If_a0;
        _ICom5 _406___mcc_h13 = _source7.dtor_If_a1;
        _ICom5 _407_c1 = _406___mcc_h13;
        _IB _408_b = _405___mcc_h12;
        bool _409_condition = false;
        _IB _source14 = _408_b;
        if (_source14.is_Eq) {
          _IM _410___mcc_h37 = _source14.dtor_Eq_a0;
          _IM _411___mcc_h38 = _source14.dtor_Eq_a1;
          _IM _412_y = _411___mcc_h38;
          _IM _413_x = _410___mcc_h37;
          bool _out12;
          _out12 = (e).Eq(_413_x, _412_y);
          _409_condition = _out12;
        } else {
          _IM _414___mcc_h39 = _source14.dtor_Elem_a0;
          Dafny.ISequence<_IM> _415___mcc_h40 = _source14.dtor_Elem_a1;
          Dafny.ISequence<_IM> _416_y = _415___mcc_h40;
          _IM _417_x = _414___mcc_h39;
          bool _out13;
          _out13 = (e).Elem(_417_x, _416_y);
          _409_condition = _out13;
        }
        if (_409_condition) {
          __default.bigstep__level5(_407_c1, e);
        }
      } else if (_source7.is_IfElse) {
        _IB _418___mcc_h14 = _source7.dtor_IfElse_a0;
        _ICom5 _419___mcc_h15 = _source7.dtor_IfElse_a1;
        _ICom5 _420___mcc_h16 = _source7.dtor_IfElse_a2;
        _ICom5 _421_c2 = _420___mcc_h16;
        _ICom5 _422_c1 = _419___mcc_h15;
        _IB _423_b = _418___mcc_h14;
        bool _424_condition = false;
        _IB _source15 = _423_b;
        if (_source15.is_Eq) {
          _IM _425___mcc_h41 = _source15.dtor_Eq_a0;
          _IM _426___mcc_h42 = _source15.dtor_Eq_a1;
          _IM _427_y = _426___mcc_h42;
          _IM _428_x = _425___mcc_h41;
          bool _out14;
          _out14 = (e).Eq(_428_x, _427_y);
          _424_condition = _out14;
        } else {
          _IM _429___mcc_h43 = _source15.dtor_Elem_a0;
          Dafny.ISequence<_IM> _430___mcc_h44 = _source15.dtor_Elem_a1;
          Dafny.ISequence<_IM> _431_y = _430___mcc_h44;
          _IM _432_x = _429___mcc_h43;
          bool _out15;
          _out15 = (e).Elem(_432_x, _431_y);
          _424_condition = _out15;
        }
        if (_424_condition) {
          __default.bigstep__level5(_422_c1, e);
        } else {
          __default.bigstep__level5(_421_c2, e);
        }
      } else {
        _ICom5 _433___mcc_h17 = _source7.dtor_Seq_a0;
        _ICom5 _434___mcc_h18 = _source7.dtor_Seq_a1;
        _ICom5 _435_c2 = _434___mcc_h18;
        _ICom5 _436_c1 = _433___mcc_h17;
        __default.bigstep__level5(_436_c1, e);
        __default.bigstep__level5(_435_c2, e);
      }
    }
    public static bool isInt(char a) {
      return ((new BigInteger(a)) - (new BigInteger('0'))) <= (new BigInteger(9));
    }
    public static BigInteger charToInt(char a) {
      return (new BigInteger(a)) - (new BigInteger('0'));
    }
    public static char intToChar(BigInteger a) {
      return (char)(((char)(a)) + ((char)('0')));
    }
    public static _IMaybe<BigInteger> strToInt(Dafny.ISequence<char> a)
    {
      _IMaybe<BigInteger> r = Maybe<BigInteger>.Default();
      if (__default.isInt((a).Select(BigInteger.Zero))) {
        r = Maybe<BigInteger>.create_Just(__default.charToInt((a).Select(BigInteger.Zero)));
      } else {
        r = Maybe<BigInteger>.create_Nothing();
      }
      BigInteger _hi3 = new BigInteger((a).Count);
      for (BigInteger _437_j = BigInteger.One; _437_j < _hi3; _437_j++) {
        _IMaybe<BigInteger> _source16 = r;
        if (_source16.is_Nothing) {
          r = Maybe<BigInteger>.create_Nothing();
        } else {
          BigInteger _438___mcc_h0 = _source16.dtor_Just_a0;
          BigInteger _439_x = _438___mcc_h0;
          if (__default.isInt((a).Select(_437_j))) {
            r = Maybe<BigInteger>.create_Just(((_439_x) * (new BigInteger(10))) + (__default.charToInt((a).Select(_437_j))));
          } else {
            r = Maybe<BigInteger>.create_Nothing();
          }
        }
      }
      return r;
    }
    public static Dafny.ISequence<char> intToStr(BigInteger a)
    {
      Dafny.ISequence<char> r = Dafny.Sequence<char>.Empty;
      r = Dafny.Sequence<char>.FromString("");
      BigInteger _440_temp1;
      _440_temp1 = a;
      while ((_440_temp1).Sign == 1) {
        BigInteger _441_temp2;
        _441_temp2 = Dafny.Helpers.EuclideanModulus(_440_temp1, new BigInteger(10));
        r = Dafny.Sequence<char>.Concat(Dafny.Sequence<char>.FromElements(__default.intToChar(_441_temp2)), r);
        _440_temp1 = Dafny.Helpers.EuclideanDivision((_440_temp1) - (_441_temp2), new BigInteger(10));
      }
      return r;
    }
  }
} // end of namespace _module
