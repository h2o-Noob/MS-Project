# E0240 Project 1 Source-Mining Report

Generated: 2026-09-05. Folder searched in full: `C:\Users\vaibhav mahore\Downloads\CSA Modelling Simulation` (333 files).

Slide references use these abbreviations: **L1** = `Lecture Slides/1_Lecture_11_08_26.pdf`, **L2** = `2_Lecture_13_08_26.pdf`, **L3** = `3_lecture_18_08_26.pdf`, **L4** = `4_lecture_20_08_26.pdf`. In L1 and L2 the printed slide number equals the PDF page number; for L3/L4 the PDF page is cited. Every claim below comes from a file in the folder; anything absent is marked NOT FOUND.

**Scope warning that shapes everything below:** only four lecture decks exist (lectures of 11, 13, 18, 20 Aug 2026). The Queuing Theory lectures (scheduled 22/09, 24/09, 29/09), "Queuing Network" (01/10), Markov Chain lectures, and "Simulation and Modelling" (03/11) are on the course timeline (L2 s3-4) but their slides are NOT in the folder. So the continuous-time machinery (M/M/1, M/M/c, M/G/1, Jackson, Burke) is NOT FOUND here; the course's own queueing material to date is discrete-time (Geo/D/1, Geo/Geo/1).

---

## 1. FOLDER MAP

### Lecture Slides/ (course material)
| File | Content |
|---|---|
| `1_Lecture_11_08_26.pdf` (32 slides) | Lecture 1, 11 Aug 2026: instructor (Sumit K. Mandal, IISc CSA), logistics, evaluation split, project phases and grading, motivation (SoC simulation, road traffic as queueing network, "Overview of Queue Simulation", course tools). |
| `2_Lecture_13_08_26.pdf` (47 slides) | Lecture 2, 13 Aug 2026: course timeline with all deadlines; "Basics of Simulation (1)": simulation definition, typical flow (with Verify/Validate steps), components of discrete-event simulation, event list, full worked single-server FIFO simulation, performance metrics, arrival-routine flowchart. |
| `3_lecture_18_08_26.pdf` (13 pages) | Lecture 3, 18 Aug 2026: random variate generation ("Slide Courtesy: Prof. R Govindarajan, Jan. 2007"): ITT (continuous and discrete), composition, convolution, acceptance-rejection (names only), exponential and geometric generation. |
| `4_lecture_20_08_26.pdf` (24 pages) | Lecture 4, 20 Aug 2026: announcements (sample projects posted), multicore/SoC/NoC background, "NoC is a Network of Queues", BookSim demo (important files listed), trace file format. |

### Projects/ (course material)
| File | Content |
|---|---|
| `list_of_sample_projects.pdf` | The 4 sample project statements for Aug'26; item 1 is Project 1, quoted verbatim in section 6. |

### Assignment1/ (course handout + your submitted work; LaTeX build artifacts grouped)
| File(s) | Content |
|---|---|
| `assignment_1.pdf`, `assignment_1.txt` | Course handout: Assignment #1, deadline "30th August, 11:59 PM", 4 problems (Geo/D/1 sweep, Geo/Geo/1 comparison, BookSim trace-based run, BookSim 8x8 synthetic run), points [10]/[15]/[15]/[10], "Please write the solution as well as put the figures in latex and submit the PDF". |
| `assignment_1_report.pdf/.tex` (+`.aux/.log/.out`) | Your Assignment 1 LaTeX report, v1 (26 Aug). |
| `assignment_1_solutions.pdf` (+`.aux/.log/.out`) | Your Assignment 1 "Solutions Report" v2 (26 Aug); contains the analytical formulas quoted in section 2 (your derivations, not course verbatim). |
| `Assignment_1_Vaibhav_Mahore.pdf`, `_Final.pdf`, `_.pdf` (+`.aux/.log/.out` each where present) | Three submission copies of your report (30 Aug, 20:56 / 21:26 / 21:37). |
| `Assignment_1_Vaibhav_Mahore_Submitted.aux/.log/.out` | Build leftovers of a "Submitted" PDF that is no longer in the folder. |
| `problem1_solution.m` / `.py` | Your Geo/D/1 simulator (MATLAB and Python), simulation-length sweep [10^2, 10^4, 10^6, 10^8]. |
| `problem2_solution.m` | Your MATLAB Geo/D/1 vs Geo/Geo/1 comparison (mean service 2). |
| `run_p1_verified.py` | Verified rerun, fixed seed 20260825, numpy `default_rng`. |
| `run_p2.py`, `run_p3.py`, `run_p4.py`, `run_p4_parallel.py` | Python drivers: P2 comparison, P3 trace generation + BookSim invocation (comment: "100K cycles as clarified by Prof. Sumit Kumar Mandal"), P4 rate sweep (serial and parallel). |
| `plot_p1.py`, `plot_p2.py`, `plot_p3_dual.py` | matplotlib figure scripts. |
| `sim_p1.cpp` + `sim_p1.exe`, `sim_p2_10e8.cpp` + `sim_p2_10e8.exe` | Your C++ single-queue simulators (`<random>`, `SimResult` struct) and compiled binaries. |
| `problem{1..4}_plot.pdf/.png` | Four output figures. |
| `problem{1..4}_results.csv`, `problem1_verified_results.csv`, `problem2_verified_10e8.csv` | Result tables with simulated vs analytical columns (validation evidence). |
| `traces_p3/trace_rate_0.1.txt` ... `trace_rate_1.0.txt` | Ten generated BookSim traces, 3 columns `src dst time` (e.g. 9976 lines at λ=0.1 over 100k cycles). |

### Simulators/ (course-provided BookSim C++ tree, ~260 files)
| File(s) | Content |
|---|---|
| `E0240_booksim_files.zip` | Zip archive of the tree below. |
| `src/Makefile` | GNU Make build; uses `LEX = flex`, `YACC = bison -y`. |
| `src/main.cpp` | Entry point; `Simulate()` builds `Network` + `TrafficManager`, calls `Run()`; usage line: `"Usage: booksim configfile... [param=value...]"`. |
| `src/booksim` | Prebuilt 64-bit Linux ELF binary (11 MB, built 26 Aug, with debug info). |
| `src/booksim_config.cpp/.hpp`, `config.l`, `config.y`, `lex.yy.c`, `y.tab.c/.h` | Configuration parser (flex/bison grammar). |
| `src/injection.cpp/.hpp` | Injection processes: `bernoulli` (test: `RandomFloat() < rate`), `on_off`, `custom`, `trace_based`. |
| `src/traffic.cpp/.hpp` | Traffic patterns (uniform, custom dest patterns, trace-based). |
| `src/trafficmanager.cpp/.hpp`, `batchtrafficmanager.*` | Central cycle-accurate loop, warm-up/sampling (`warmup_periods`, `sample_period`, `max_samples`), stats collection. |
| `src/random_utils.cpp/.hpp`, `rng.c`, `rng-double.c`, `rng_wrapper.cpp`, `rng_double_wrapper.cpp` | RNG: Knuth `ran_array` lagged Fibonacci (public domain, TAOCP Seminumerical Algorithms 3.6); `RandomSeed/RandomInt/RandomFloat`. |
| `src/stats.cpp/.hpp` | Performance statistics accumulation. |
| `src/networks/*` (11 modules) | Topologies: `kncube` (mesh/torus), `cmesh`, `dragonfly`, `fattree`, `flatfly_onchip`, `fly`, `anynet`, `qtree`, `tree4`, base `network`. |
| `src/routers/*` (4 modules) | `iq_router` (input-queued), `event_router`, `chaos_router`, base `router`. |
| `src/allocators/*` (9 modules) | VC/switch allocators: `islip`, `pim`, `loa`, `maxsize`, `selalloc`, `separable`, `separable_input_first`, `separable_output_first`, `wavefront`. |
| `src/arbiters/*` (4 modules) | `roundrobin_arb`, `matrix_arb`, `prio_arb`, `tree_arb`. |
| `src/power/*`, `techfile.txt` (x2), `extract_area_power.py` | Power/area modelling add-on with monitors and technology file. |
| `src/buffer.*`, `buffer_state.*`, `vc.*`, `flit.*`, `flitchannel.*`, `credit.*`, `channel.hpp`, `outputset.*`, `routefunc.*`, `module.*`, `timed_module.hpp`, `misc_utils.*`, `config_utils.*`, `packet_reply_info.*`, `pipefifo.hpp`, `globals.hpp`, `booksim.hpp` | Core plumbing: buffers, virtual channels, flits, credits, routing functions, event/time modules. |
| `src/examples/` (11 files) | Stock example configs: `singleconfig` (10x10 crossbar fly), `mesh88_lat`, `fattree_config`, `dragonflyconfig`, `cmeshconfig`, `flatflyconfig`, `torus88`, `anynet/` (README + arbitrary-topology files). |
| `src/mesh_config_trace_based` | Course config for trace mode: mesh `k=5, n=2` (header comment says "8X8 mesh"), `traffic = trace_based`, `injection_process = trace_based`, `routing_delay/vc_alloc_delay/sw_alloc_delay/st_final_delay = 1`, `num_vcs = 1`, `buf_size = 10`, `sim_type = latency`, `sample_period = 1000000`, `warmup_periods = 0`, `max_samples = 1`. |
| `src/mesh_config_p4` + `mesh_config_p4_0.01` ... `_0.10` (11 files) | Sweep configs for Assignment 1 P4: mesh `k=8, n=2`, `traffic = uniform`, `injection_process = bernoulli`, `warmup_periods = 0`, `sample_period = 1000000`, per-file `injection_rate`. |
| `src/trace_file.txt` | 100000-line example trace, `0 1 t` per line. |
| `src/watch_file.txt`, `watch_flits.txt`, `watch_out.txt`, `watch_out_south_prio.txt` | Flit-watch debug outputs (course-instructor artifacts). |
| `src/tags.lst`, `cscope.out`, `grep.exe.stackdump` | Editor/dev artifacts. |
| All `*.o` (56) and `*.d` (54) files | Compiled objects and dependency files from a prior Linux build. |

### toy_examples/toy_examples/single_queue_simulation/ (course class code)
| File | Content |
|---|---|
| `single_queue_simulation_geo_d_1.m` | The in-class single-queue simulator the assignment refers to: cycle-driven Geo/D/1, Bernoulli arrival (`rand <= injection_rate`), service countdown, returns `average_occupancy` and `average_utilization` as time averages. |
| `top_script.m` | Driver: `service_time = 3`, `injection_rate_array = [0.05:0.05:0.45, 0.49]`, `simulation_length = 1000000`, plotting style, plus commented-out analytical formulas (quoted in section 2). |

---

## 2. QUEUEING THEORY CONTENT

### What IS in the folder

**Queue models actually covered: Geo/D/1 and Geo/Geo/1 (discrete-time), plus a queueing-network picture.** M/M/1, M/M/c, M/G/1, open/closed Jackson networks, Burke's theorem: NOT FOUND (keyword sweep over every text-bearing file returns zero hits; those lectures are scheduled 22/09 to 01/10 per L2 s3-4 but their slides are absent).

**Course notation (verbatim sources):**

- L2 s14-17 (single-server simulation): "ti - arrival time of i-th customer", "Ai - inter-arrival time of i-th customer = (ti - ti-1)", "Si - service for i-th customer", "Di - Delay in queue of i-th customer". L2 s29 adds: "D(t), Q(t), B(t) - Delay, Queue Length, Utilization".
- L1 s21 ("Overview of Queue Simulation"): "Objective: To know average occupancy. Need to know: Input distribution, Service time distribution, Number of servers. Summary: need a good hold of stochastic process". This is the instructor's own definition of the key performance metric for exactly this project: average occupancy.
- L1 s27 ("Road as a Queuing Network"): queues Q1-Q4 fed by roads R1-R4, each queue annotated with pairs "(λ, Ca)" and "(μ, Cs)", indexed variants "(λ1, Ca1), (μ1, Cs1)" etc. Ca and Cs are never defined anywhere in the folder.
- Assignment 1 (`assignment_1.pdf`): Kendall notation "Geo/D/1" and "Geo/Geo/1"; λ is called "injection rate", in "packets/cycle", Bernoulli per-cycle arrivals.
- `top_script.m` (course code, commented lines): `rho = injection_rate*service_time;` i.e. ρ = λS.

**Formulas VERBATIM from course files:**

- L2 s19-21, 43-45 (performance metrics, the ones the simulator must output):
  - "Average Delay = ( Σ Di ) / n" with the worked value "= 41/5 = 8.2"
  - "Average queue length = ( Σ I * Ti ) / T" with the worked value "(5*1 + 2*2 + 2*3 + 7*2 + 2*1) / 25 = 31/25 = 1.24", and the emphasis "Avg. Queue length is a time-average!"
  - L2 s23: "Server Utilization - Time Average = (time for which server is busy/total time) = (23/25) = 0.92"
- `top_script.m` (commented analytical formulas, course-authored):
  - `waiting_time_analytical(injection_rate_idx) = 0.5*rho*(service_time - 1)/(1 - rho);` i.e. Wq = ρ(S - 1) / (2(1 - ρ)) for Geo/D/1
  - `waiting_time_simulation(injection_rate_idx) = average_occupancy(injection_rate)/injection_rate;` i.e. W = Lq/λ. This is Little's Law applied, but it is never named anywhere in the folder (zero hits for "Little").
- L3 s9-10 (random variates, needed to build these queues): "Since F(x) lies in the range [0,1], assign F(x) = U(0,1)... Return X = F^-1(U)"; for exponential: fx = λe^(−λx), Fx = 1 − e^(−λx), "X = (−1/λ) ln(1 − U)".

**Formulas from your own accepted Assignment 1 report** (`assignment_1_solutions.pdf`; flagged: these are your derivations, not course-verbatim, though they match the course code's commented formula at S=2):

- Geo/D/1 mean waiting-queue length: Lq = λ²(S - 1)/(1 - λS), which " = λ²/(1 − 2λ)" for S = 2 (Eq. 1).
- Discrete-time Pollaczek-Khinchine (Eq. 2): Lq = λ²(Var(S) + E[S]² - E[S]) / (2(1 − ρ)).
- Geometric service variance: Var(S) = (1 - ps)/ps² = 2 for ps = 0.5; hence Lq(Geo/Geo/1) = 2λ²/(1 - 2λ) = 2 x Lq(Geo/D/1) (Eq. 3).
- Overload backlog delay (P3): W̄ = (1/2)(λ/μ - 1)T, with μ = 1/3 for the BookSim single flow.
- 8x8 mesh mean hop count (P4): H̄ = 2(k² - 1)/(3k) = 2 x 63/24 = 5.25.

**If you validate against M/M/1, M/M/c, or Jackson results, that validation basis is NOT in the folder.** The only analytically validated models with course backing are Geo/D/1 and Geo/Geo/1 above, plus the generic metric definitions of L2 s19-23.

---

## 3. SIMULATION METHODOLOGY

Everything the folder teaches on this:

- **Definition and model abstraction** (L2 s7-8): simulation imitates key characteristics of a system; "System model: Abstraction of real system... Simplifying assumptions capture only important behaviors"; time may be compressed or expanded.
- **Simulation flow** (L2 s9): "Problem Formulation -> Setting of Objectives -> Develop Model -> Data Collection -> Translate Model -> Verify -> Validate -> Exptl. Design -> Production Run & Anal. -> Output & Document". Verify and Validate appear as two separate boxes (see section 4).
- **Components of discrete-event simulation** (L2 s10), verbatim list: "System State: collection of state variables; Simulation Clock: current value of simulated time; Stat. counters: variables used for system performance; Initialization Routines: initialize relevant counters; Timing Routine: for determining next event; Event Routine: collection of state variables; Library Routine: collection of routines for probability distributions".
- **Time advance** (L2 s11): "Event Queue: holds events in chronological (increasing time) order"; two schemes contrasted: "Next-event time: Simulation time updated to next-event time" and "Fixed-increment time advance: Simulation time incremented by a fixed amount. Many increments before an actual event!"
- **Program skeleton** (L2 s12), verbatim pseudocode: `Initialize(); While (1) { Invoke timing routine; Invoke Event routine; } Output Result;` with `Timing Routine() { Determine next event; Advance Sim. Time; }` and `Event Routine() { Update sys. state; Update stat. counters; Generate and add new event to event queue; }`.
- **Event-handling walkthrough** (L2 s26-40): a 5-customer run (arrival times 1, 4, 9, 11, 24; service times 13, 7, 2, 1, 1) traced step by step with an explicit Event List holding "A-t" (arrival at t) and "D-t" (departure at t) entries, Server Status, Q. Len, Clock. Departure events generated as "D-13, D-20, D-22, D-23, D-25".
- **Arrival routine logic** (L2 s46, flowchart): on arrival, schedule next arrival; if server busy, add 1 to queue and store arrival time; else set Delay = 0, make server busy, schedule departure event, add 1 to delayed customers.
- **Random variate generation** (L3): four named techniques: "Inverse transformation technique, Composition method, Convolution method, Acceptance-rejection method" (s4-5); only ITT is worked out: continuous ITT X = F⁻¹(U) (s9), exponential derivation (s10), discrete ITT "Determine the smallest positive integer I such that U ≤ F(I)" with a 3-value pmf example (s11), and Bernoulli/geometric generation: "Generate a packet with probability of success λ... Generate packet if U(0,1) < λ" with example λ = 0.2 (s12).
- **Warm-up periods:** NOT FOUND as taught methodology. Proxies only: BookSim configs set `warmup_periods = 0` with `sample_period = 1000000`, `max_samples = 1` (`mesh_config_trace_based`, `mesh_config_p4*`); the Assignment 1 P1 report notes short runs are "biased by starting from an empty queue" and convergence at 10^6 to 10^8 cycles.
- **Number of replications, confidence intervals, variance reduction, output analysis, terminating vs steady-state:** NOT FOUND. Zero hits for "confidence", "replication", "variance reduction", "steady state" across all files. The course's convergence device is simulation-length sweeps (Assignment 1 P1: lengths [10^2, 10^4, 10^6, 10^8]), not replication + CI.

Note the course practice vs. lecture contrast: L2 teaches the event-driven skeleton, but the course's own class code (`single_queue_simulation_geo_d_1.m`) is fixed-increment (cycle-driven) discrete-time simulation. Both paradigms are therefore "course-sanctioned"; the trace/occupancy conventions come from the MATLAB code.

---

## 4. VERIFICATION & VALIDATION

- The only V&V "definition" is structural: L2 s9's simulation flow places "Verify" and "Validate" as two distinct steps between "Translate Model" and "Exptl. Design". No definitions, checklists, methods, or rubric for V&V exist anywhere in the folder: NOT FOUND beyond this.
- The word "verify" in course documents: sample project 2 ("Modify the simulator to incorporate a new feature and verify the feature") and sample project 4 ("Construct a simulator as well as models for distributed system. Verify the simulator with the model."). Project 1's own text does not use the word; it says "construct a simulator... capture key performance metric (e.g., queue occupancy)". By course pattern (project 4) and Assignment 1 practice, verification means agreement between simulated metrics and analytical model values: the accepted assignment compares simulated vs analytical columns (e.g. `problem2_verified_10e8.csv`, errors under 0.1%, and "closely matching the simulated 10,439.7 cycles" in P3).
- No V&V grading rubric: NOT FOUND. The general evaluation criteria that would apply are "Correctness, Clarity, Conciseness" plus "research rigor" (L1 s7, s11).

---

## 5. TOOLS & CODE

- **No SimPy anywhere** (zero hits). No Python simulation framework at all.
- **MATLAB is the course's language for queue simulation**: the in-class code is `single_queue_simulation_geo_d_1.m` + `top_script.m` (cycle-based, `rand` for Bernoulli draws, occupancy and utilization as time averages). Assignment 1 P3 explicitly says "imitates single queue simulation (as in the Matlab code)".
- **C++ is the course's simulator language**: BookSim 2.0 source tree (flex/bison config parsing, GNU Make). L4 s22, verbatim: "A cycle accurate NoC simulator. Input: A config file consisting of all design parameters. Output: Performance numbers. Important directory/functions/files to note: main.cpp, examples, booksim_config.cpp, traffic.cpp, trafficmanager.cpp". Invocation: `booksim configfile... [param=value...]`.
- **Allowed languages, L1 s6 verbatim**: "Coding: MATLAB, Python, C/C++,…..". Your own accepted assignment used all three (Python numpy/pandas/matplotlib, C++ `<random>`, MATLAB).
- **Starter code present**: the two MATLAB toy files (the canonical single-queue simulator) and the whole BookSim tree with 11 ready sweep configs (`mesh_config_p4_0.01` to `_0.10`) and `mesh_config_trace_based`. RNG in BookSim is Knuth's lagged-Fibonacci `ran_start` with `RandomSeed/RandomInt/RandomFloat`; injection processes available: `bernoulli`, `on_off`, `custom`, `trace_based`.
- **Plotting conventions (course-imposed)**: Assignment 1 requires figures in LaTeX in the PDF; "You should have 4 lines with distinct markers... in the figure where each line corresponds to a simulation length". The class MATLAB style: `plot(injection_rate_array, average_occupancy, '^k--','MarkerSize',12,'LineWidth',2)`, axis labels with units: `xlabel('Injection Rate (packets/cycle)')`, `ylabel('Average Occupancy')`, `grid on`, `box on`. X-axis is always injection rate swept; y-axis the metric (occupancy or latency).
- **Report format** (from L1 s6, assignment text, and the accepted template): PDF via LaTeX, 11pt article; title block with "Name / SR No. / Department (CSA) / Indian Institute of Science, Bangalore / Submission Date"; per-problem sections "Simulation Setup", "Theoretical Verification", "Observations". L1 s32 lists course tools: "Latex, Weka, Origin".
- **Trace file convention** (L4 s23, verbatim): "Three columns: Source router, Destination router, Time stamp. Routers cannot send more than one packet at once cycle. Number of lines in the trace file represents number of packets."

---

## 6. PROJECT REQUIREMENTS

**The project statement** (`Projects/list_of_sample_projects.pdf`, "Sample projects for E0240 (Aug'26)"), verbatim, item 1: "Collect a queuing network for any real time system and construct a simulator for the network. The simulator should capture key performance metric (e.g., queue occupancy) of the network." Sibling items for context: 2) modify an existing simulator (gem5, booksim) and "verify the feature"; 3) design-space exploration; 4) "Construct a simulator as well as models for distributed system. Verify the simulator with the model."

**Weight and structure** (L1 s10-11, verbatim unless quoted):
- "Project (40%)" of the 100% grade (Assignments 30%, Quiz 10%, Class participation 20%).
- "Semi-open ended. Must be relevant to the course material. You need to apply at least 20% of the material taught in the course to do your project."
- "Group project. Group size depends on class size." "The 'group' will be evaluated, Not the individuals."
- Three phases with weights of the 40%: "Phase-1: Describing the problem statement (5%)", "Phase-2: Progress so far (15%)", "Phase-3: Final outcome of the project (20%)".
- Phase deliverables, verbatim: "Phase-1: Submit a 2-page problem statement. Should answer the question 'why' are you doing this?"; "Phase-2: Submit a 3-page progress report. Should answer 'how' are you doing this?"; "Phase-3: Submit a 4-page report and presentation. 'What' have you done?"
- Evaluation criteria: "Correctness, clarity, conciseness, *research rigor*". "Points range: [-x, x] where x is the maximum point."
- **Deadlines** (L2 s3-5 timeline, verbatim): Phase-1 due 22/09 (same day as "Queuing Theory (1)"); Phase-2 due 27/10; Final Presentations on 16/11, 17/11, 19/11; "Final report submission/end-term" 26/11. Decision between project and exam was due 1st September (L1 s12, L4 s2). As of 05/09/2026, the next deliverable is the 2-page Phase-1 statement by 22 September 2026.
- **What "construct" and "key performance metric" mean to this instructor**: no explicit rubric definition exists (NOT FOUND). The operative definitions come from L1 s21 ("Objective: To know average occupancy") and the class simulator's outputs (`average_occupancy`, `average_utilization`): queue occupancy as a time-average is the exemplary key metric, exactly as the project text says "(e.g., queue occupancy)". "Construct a simulator" in course practice means writing the simulator code (MATLAB/Python/C++ style of Assignment 1), in contrast to sample projects 2-3 which use existing simulators.
- **Presentation**: Phase-3 includes a presentation (L1 s11); dedicated presentation days on the timeline. Report length: 4 pages for Phase-3 (2 and 3 for Phases 1-2).
- Announcements channel: L4 s2, "List of sample projects have been posted in teams"; course runs on Teams (L1 s4). Teams content (including any rubric posted there) is NOT in this folder.

---

## 7. INSTRUCTOR EMPHASES / TRAPS

1. **Deadlines are absolute.** L1 s4: "Absolutely no extension of deadlines", and "Unfairness is a part of life unfortunately". Phase-1 on 22/09 is the hard next date.
2. **Negative marks are real.** L1 s11: "Negative points will be awarded if very high marks is obtained in assignment but absolutely no rigor in the project submissions (risk)". A strong Assignment 1 score raises the rigor expectation: analytical validation, not just plots.
3. **Similarity penalty.** L1 s7: AI use is allowed ("You can even *blatantly copy-paste* from AI tool with your own risk") but "Heavy penalty based on similarity score between class". The report must not read like classmates'.
4. **The 20% rule.** The project "Must be relevant to the course material" and must "apply at least 20% of the material taught in the course" (L1 s10). Anchor the write-up in course concepts by name: discrete-event components (L2 s10), event list, time-average occupancy, ITT/Bernoulli generation, Geo/D/1 vs Geo/Geo/1, BookSim if used.
5. **Grading triad everywhere.** "Correctness, Clarity, Conciseness" (L1 s7) and "research rigor" (L1 s11): keep reports inside the page caps (2/3/4), with setup, verification against formulas, and observations sections, exactly like the accepted Assignment 1 format.
6. **Figures must be in LaTeX, PDF only, not handwritten** (Assignment 1: "Please write the solution as well as put the figures in latex and submit the PDF"; L1 s6: "not handwritten and scanned"). Distinct markers per line in multi-line plots is an explicit assignment requirement and a safe convention for project figures.
7. **Simulation length matters more than replications.** The course's own device for statistical adequacy is sweeping simulation length (10^2 to 10^8 in A1 P1) and noting convergence to analytical values; there is no confidence-interval requirement anywhere in the folder (NOT FOUND). Do not burn effort on CI machinery the course never asked for; do show run-length/convergence evidence.
8. **Time-average, not sample-average, for occupancy.** L2 s21 stresses "Avg. Queue length is a time-average!"; the class code implements it as `occupancy_counter/simulation_length`. Getting this wrong breaks validation against Lq = λ²/(1 - 2λ).
9. **Config discipline.** A1 P4: "Do not change any parameter in the configuration file unless it is related to synthetic traffic and simulation length." Expect the same strictness: state and justify every parameter changed in any simulator.
10. **50% board work.** L1 s4: "Almost 50% of the lectures will be done through board-work. Make sure to take notes." Much of the queueing derivation (including the Geo/D/1 formula, which appears only as a commented line in `top_script.m`) lives on the board, not in slides: the missing M/M/1 and Jackson material will likely be board-derived in the 22/09 to 01/10 lectures, worth attending before finalizing validation targets.
11. **Class participation is 20%.** L1 s9: "If you are silent, you are not learning". Asking about Project 1 specifics (network choice, validation expectations) is itself graded behavior.
12. **Notation fidelity.** The course writes queueing networks with (λ, Ca), (μ, Cs) pairs per node (L1 s27) and calls λ "injection rate" in "packets/cycle". Mirroring course notation and terminology (occupancy, injection rate, Geo/.../1) in the report costs nothing and signals the 20% course-material linkage.

---

## CONTEXT DIGEST

Course: E0240 Modeling and Simulation, IISc CSA, Aug 2026, instructor Sumit K. Mandal. Project 1 (from `Projects/list_of_sample_projects.pdf`): "Collect a queuing network for any real time system and construct a simulator for the network. The simulator should capture key performance metric (e.g., queue occupancy) of the network." Project = 40% of grade, group-based, three phases: 2-page problem statement ("why", 5%) due 22/09/2026; 3-page progress report ("how", 15%) due 27/10; 4-page report plus presentation ("what", 20%), presentations 16-19/11, final report 26/11. Graded on "Correctness, clarity, conciseness, research rigor"; points can be negative; no deadline extensions; similarity between classmates heavily penalized; must apply at least 20% of course material.

Folder holds only 4 lecture decks (11-20 Aug). Continuous-time queueing (M/M/1, M/M/c, M/G/1, Jackson, Burke, Little's Law) is NOT FOUND; those lectures come later (22/09 to 01/10). Course queueing to date is discrete-time: Geo/D/1 and Geo/Geo/1, with λ = injection rate (packets/cycle), ρ = λS. Canonical formulas: Geo/D/1 Wq = ρ(S-1)/(2(1-ρ)); Lq = λ²(S-1)/(1-λS) = λ²/(1-2λ) for S=2; discrete P-K: Lq = λ²(Var(S)+E[S]²-E[S])/(2(1-ρ)); Geo/Geo/1 with mean service 2 gives exactly 2x Geo/D/1 occupancy. Metric definitions (L2 s19-23): Average Delay = (ΣDi)/n; Average queue length = (Σ Ii*Ti)/T, a time-average; Server Utilization = busy time/total time. Network notation (L1 s27): per-node (λ, Ca), (μ, Cs). Objective per instructor: "to know average occupancy"; inputs needed: arrival distribution, service distribution, number of servers.

Simulation methodology taught (L2): components (system state, clock, stat counters, timing/event/library routines); event queue in chronological order; next-event vs fixed-increment time advance; program skeleton Initialize, While(1){timing routine; event routine}, with event routine updating state, counters, and scheduling new events. Class code is cycle-driven MATLAB (`single_queue_simulation_geo_d_1.m`): Bernoulli arrival if rand ≤ λ, deterministic service countdown, occupancy_counter/simulation_length. RNG taught (L3): ITT X = F⁻¹(U), exponential X = (-1/λ)ln(1-U), discrete ITT smallest I with U ≤ F(I), geometric via U < λ. Warm-up, replications, confidence intervals, variance reduction: NOT FOUND; course practice is simulation-length sweeps (10^2 to 10^8) converging to analytical values. V&V: only the flow chart's separate Verify/Validate steps (L2 s9) and the course habit of validating simulated metrics against analytical formulas (as in Assignment 1, errors < 0.1%).

Tools: no SimPy. Course uses MATLAB (queue sim), C++ (BookSim NoC simulator, cycle-accurate, config-file driven; key files main.cpp, booksim_config.cpp, traffic.cpp, trafficmanager.cpp), and permits "MATLAB, Python, C/C++". Reports in LaTeX PDF; plots with distinct markers, labeled "Injection Rate (packets/cycle)" vs "Average Occupancy"; trace files are "src dst time" triplets. Validate the simulator against Geo/D/1 and Geo/Geo/1 closed forms and time-average occupancy; present run-length convergence; mirror course notation and terminology.
