# Run your first Qutes program

Save the following as `bell.qut`. It prepares two qubits and returns their measurements in the order `[alice, bob]`.

```qutes
qubit alice = false;
qubit bob = false;
hadamard(alice);
if (alice) { not(bob); }
return [measure(alice), measure(bob)];
```

## In the browser

Open the [Bell experiment](https://qutes-lang.web.app/play.html#bell) and select **Run**. Its helper function performs the same two gates. With 64 shots you should see only matching pairs. The counts beside them can vary. Open **Circuit** and select a gate to locate its source.

## In VS Code

Install the [Qutes extension for desktop VS Code](https://marketplace.visualstudio.com/items?itemName=GabrieleMessina.qutes). It includes the compiler and simulator for supported systems. Open the file and use the play button or **Qutes: Run Qutes File**. Use **Qutes: Set Shot Count** to change the number of repetitions.

## In a terminal

Choose your archive on the [Downloads page](https://qutes-lang.web.app/downloads.html), extract the whole folder and open a terminal there. The archive already includes a Bell example.

| System | Command from the extracted folder |
| --- | --- |
| Windows PowerShell | `.\qutes.exe run examples\bell.qut --shots 64` |
| macOS or Linux | `./qutes run examples/bell.qut --shots 64` |

To run your own file, replace the example path with the path to `bell.qut`. Keep the executable with its bundled libraries. For inputs and output files, see the [command-line reference](cli.md).
