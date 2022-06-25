# hedyindafny

hedy1.cs is the C# file hedy1.dfy compiles to, etc.

hedy1.dfy, hedy2.dfy, hedy3.dfy, hedy4.dfy and hedy5.dfy contain the semantics of Hedy level 1, 2, 3, 4 and 5 respectively, I think it is now complete and without errors. 

hedy4.dfy contains the semantics of Hedy level 4. It is exactly the same as the code for level 3, except for the method substStr, this method works a little bit different here, because of syntactic changes in Hedy. The semantics does not change from level 3 to 4.

oldapproachhedy.dfy contains an old approach for implementing the semantics. This might be useful if someone continues this work of implementing the semantics of Dafny in Hedy. This approach can be helpful for the next step of verifying the implementation, so that the Dafny code can be used as a reference implementation. The approach taken here is similar to: https://www.cs.cmu.edu/~mfredrik/15414/lectures/11-notes.pdf

hedy1-properties.dfy and hedy1-tree.dfy contain attempts to verify the implementation of the semantics of Hedy level 1, so that the Dafny code can be used as reference implementation.
