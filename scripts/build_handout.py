"""Build the English assignment handout with ReportLab."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
story = []


def paragraph(text, size=11, bold=False, center=False):
    style = ParagraphStyle("text", fontName="Times-Bold" if bold else "Times-Roman",
                           fontSize=size, leading=size*1.24, alignment=1 if center else 0)
    return Paragraph(text, style)


def body(text):
    story.extend([paragraph(text), Spacer(1, 7)])


def heading(text):
    story.extend([paragraph(text, 15, True), Spacer(1, 7)])


def problem(key, name, points, parts):
    rows = [[paragraph(f"Problem ({key}): {name} ({points} points)", 11, True)]]
    for i, (score, prompt, evidence) in enumerate(parts):
        rows.append([paragraph(f"<b>({chr(97+i)})</b> {prompt} ({score} points)<br/>"
                               f"<b>Deliverable:</b> {evidence}", 10.6)])
    assert sum(p[0] for p in parts) == points
    table = Table(rows, colWidths=[468], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BOX",(0,0),(-1,-1),.9,colors.HexColor("#ff8800")),
        ("LINEBELOW",(0,0),(-1,0),.4,colors.grey),
        ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story.extend([table, Spacer(1, 10)])


story.extend([paragraph("Assignment 1 (basics): Coordinating Wind, Solar and Storage",19,True,True),
              Spacer(1,8),paragraph("Sustainable Energy  ·  Applied AI Project",13,False,True),
              paragraph("Student handout  ·  Framework review edition",11,False,True),Spacer(1,22)])
heading("1   Assignment overview")
body("A region can import up to 35 MW. At noon, wind and solar can cover demand and charge two stores. By evening the same region may depend on the water and battery energy it saved. When does a better forecast change the first-hour decision? When does a supervisor improve on deterministic planning?")
body("<b>Choose one track.</b> Track A measures the operational value of a forecast. Track B measures the value of a supervisory tool loop. Each track totals 100 points: 35 for implementation, 25 for energy engineering, 25 for experiments and 15 for reproducibility. The last problem is common to both.")
heading("1.1   System and information boundary")
body("Use the RTE national wind, solar and demand series as drivers of a virtual single-bus system. Convert timestamps to UTC. Average two valid half-hour MW observations per target and retain missing hours on the time axis. Preserve night-time solar zeros. Fit scaling on joint-valid 2019-2022 hours: map wind and solar maxima to 80 and 60 MW and cap at those ratings. Map the demand 99th percentile to 60 MW and leave demand uncapped.")
body("Tune on 2023 and freeze before 2024 evaluation. Assign windows by all 24 target timestamps. At hour t, the latest observation is t-1. Issue the next 24 forecast hours, replan hourly and execute only the first action. Update the reserve policy every six hours or on a published event.")
body("Initialize the battery at 10 MWh and upper reservoir at 110,000 cubic metres in every episode. Battery power is limited to 10 MW with 2-18 MWh internal energy and 95% efficiency each way. The 20 MW hydro machine has a 200 m head, a 220,000 cubic metre active reservoir and 90% efficiency each way. Each device uses one mode per hour. Grid export is zero.")
heading("1.2   A pencil-and-paper check")
body("For one hour, wind supplies 35 MW and solar supplies 20 MW. Demand is 40 MW, the pump draws 10 MW and the battery charges at 5 MW. Verify the bus residual, the change in each store and the 1.25 MWh conversion loss. For a second check, pump at 20 MW for an hour: the water gained is about 33,027.52 cubic metres and can later return 16.2 MWh to the bus.")
story.append(PageBreak())
heading("2   Track A: Probabilistic forecasting")
body("Use 168 consecutive hours to forecast the next 24. Return wind, solar and load in MW at quantiles 0.1, 0.5 and 0.9. Future calendar features use Europe/Paris local time. At inference, the evaluator supplies only revealed history and known calendar inputs.")
problem("forecast","Train and expose the predictor",35,[
(15,"Train a multivariate patch Transformer and expose its inference function.","Training log, checkpoint hash and a call through tests/adapters.py."),
(10,"Produce 24 ordered, finite quantile triples for each target and use a probabilistic training objective.","A forecast packet with issue time, target times, model hash, forecast ID and values of shape [24, 3, 3]."),
(10,"Compare daily or weekly persistence with a linear multi-step baseline.","Validation-based baseline selection, training curves and frozen settings.")])
problem("forecast_energy","Account for dispatch consequences",25,[
(8,"Explain the MW aggregation, virtual scaling and available information.","Data card with units, invalid hours, clipping and split-specific window counts."),
(9,"Trace errors in two windows through the common planner and settlement.","Aligned forecasts, realized net load, grid purchases, storage action and unserved energy."),
(8,"Reconcile a physical ledger and explain the hourly approximation.","One recomputable hour including losses and terminal restoration deficits.")])
problem("forecast_evidence","Isolate forecast value",25,[
(8,"Keep future observations outside each decision and every training label inside its split.","Timestamp audit and frozen split definitions."),
(8,"Compare seasonal A0, linear A1 and deep A2 with the same deterministic MPC.","Forecast-value table with per-target MAE, RMSE, lead 1/6/24 errors, pinball loss, coverage and width, alongside dispatch outcomes."),
(9,"Ablate a feature or loss component and investigate one failure.","A controlled comparison and a timestamped explanation of its consequence.")])
body("Use every valid sealed 2024 window for forecast metrics. Report daylight solar and net-load behavior separately. The packaged validation day illustrates the raw measurements; it is too short for a 168-hour input window.")
story.append(PageBreak())
heading("3   Track B: Bounded supervisory control")
body("The supervisor selects flexible, balanced or reserve. Their soft targets are 30%, 50% and 70% of nominal battery energy and full hydro potential. The shared mixed-integer MPC determines power. Expose observe, plan_dispatch, simulate, validate and commit through versioned interfaces; expose the current hour's actuals only at settlement.")
problem("supervisor","Implement the supervisor",35,[
(15,"Connect the tool loop and track plan, forecast and state versions.","A complete observe-to-commit trace with the selected policy and first action."),
(10,"Validate independently, recover from a tool failure and make repeated commits idempotent.","Timeout or stale-plan replay; demonstrate a single state transition on duplicate commit."),
(10,"Bound each decision to six model calls, three candidates and one correction, with a 60-second request timeout.","Complete JSONL traces, budgets, fallback reasons and original versus executed actions.")])
problem("control_energy","Verify physical operation",25,[
(10,"Audit the bus, water, energy, power limits and exclusive modes.","Hourly residuals within 1e-6 MW and 1e-3 cubic metres and independent boundary checks."),
(8,"Reconcile first-hour execution against actuals and check both terminal targets.","Executed ledger, adjustments, final stores and separately reported shortfalls."),
(7,"Explain two policy decisions using the evidence available at the time.","Two traces with expected effects, realized outcomes and limits of the hourly model.")])
problem("control_evidence","Isolate management value",25,[
(10,"Compare deterministic candidate search B0, single-choice LLM B1 and full harness B2 using a frozen predictor, common MPC, candidate set and execution rules.","Management-value table for typical, tight and volatile 72-hour episodes."),
(6,"Repeat each LLM configuration at least twice under fixed settings.","Means and ranges, tokens, model requests, latency, solver time and failures."),
(9,"Ablate correction or recovery and inject a reproducible failure.","Paired outcomes and a trace showing detection, fallback and state progression.")])
body("Freeze episode rules on validation. Compare feasible runs by unserved energy first, then terminal deficits, then operating cost plus the common curtailment cost. Exclude policy-specific reserve penalties from the comparison.")
story.append(PageBreak())
heading("4   Reproduction and submission")
problem("reproduce","Make the experiment replayable",15,[
(6,"Provide commands to reproduce the selected track and rebuild its table.","Code, configuration, dependency versions, hardware and runtime."),
(4,"Identify the data and frozen model or supervisor used.","Snapshot checksum, license, UTC rules and checkpoint or prompt, schema, gateway model ID and request parameters."),
(5,"Explain the evidence and document individual contributions.","A 3-5 page report, an eight-minute defense and a contribution statement.")])
heading("4.1   What to submit")
body("Supply the code and frozen configuration, forecast-value and management-value tables from the paired tracks, a labelled time series and one worked physical ledger. Submit hourly CSV rows and JSONL tool traces where applicable. Distinguish your own track from the frozen partner component. Include the ablation, failed runs and limitations.")
body("For each management episode record energy not served (MWh), hours with shortfall, imports and peak import, wind and solar curtailment, battery and hydro throughput, losses and terminal deficits. Break operating cost into import cost and battery throughput cost in teaching currency units. Record initial states and preserve the planned and executed action separately.")
heading("4.2   Reading a result")
body("A deep model can lower average forecast error and still miss the evening when grid import is binding. A supervisor can spend more requests and reach the same first-hour decision as B0. Both are valid outcomes. Support the conclusion with the hours, states and evidence that distinguish those cases.")
body("Invalidate and re-evaluate results affected by future-data leakage, incorrect energy units or unaccounted depletion of initial storage. Record any post-test changes. Each member should be able to recompute a time step and explain one design decision.")
heading("4.3   Review checkpoint")
body("This release supplies the public sample, course settings, storage checks and student interfaces. The sealed snapshot, numerical planner, settlement evaluator, gateway experiments and measured result tables belong to the next phase. Consult README.md for the local review sequence.")
doc = SimpleDocTemplate(str(ROOT / "docs/assignment1_energy_basics.pdf"), pagesize=letter,
                        leftMargin=66,rightMargin=66,topMargin=48,bottomMargin=43,
                        title="Assignment 1 (basics): Coordinating Wind, Solar and Storage")
def footer(canvas, doc):
    canvas.setFont("Times-Roman",10)
    canvas.drawCentredString(306,28,str(doc.page))
doc.build(story,onFirstPage=footer,onLaterPages=footer)
