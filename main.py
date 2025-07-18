from workstation.graph.builder import build_graph
import os

if __name__ == "__main__":
    print("--- Starting Autonomous Financial Research Workstation ---")
    
    company_ticker = "MSFT"
    research_topic = "Microsoft's competitive position against Google and Amazon in the AI space"
    app = build_graph()

    initial_input = {
        "ticker": company_ticker,
        "topic": research_topic
    }

    # Run the entire workflow
    final_state = app.invoke(initial_input)

    print("\n\n--- Workflow Complete ---")
    
    # Save the final report to a file
    final_report_path = final_state.get("report_path", "")
    if final_report_path:
        print(f"\n✅ Final report has been saved to: {final_report_path}")
    else:
        print("\n❌ No final report was generated.")
