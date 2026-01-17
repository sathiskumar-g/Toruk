#!/usr/bin/env python3
"""
JSON to Table Converter
Converts TORUKMACTO research JSON files to readable table format
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def format_table_row(data: List[str], widths: List[int]) -> str:
    """Format a table row with proper column widths"""
    return "│ " + " │ ".join(
        str(item)[:width].ljust(width) for item, width in zip(data, widths)
    ) + " │"


def format_table_separator(widths: List[int], style: str = "middle") -> str:
    """Format table separator line"""
    if style == "top":
        return "┌─" + "─┬─".join("─" * width for width in widths) + "─┐"
    elif style == "middle":
        return "├─" + "─┼─".join("─" * width for width in widths) + "─┤"
    elif style == "bottom":
        return "└─" + "─┴─".join("─" * width for width in widths) + "─┘"


def convert_opportunities_to_table(opportunities: List[Dict[str, Any]], max_rows: int = None) -> str:
    """Convert opportunities list to formatted table"""
    
    if not opportunities:
        return "No opportunities found in JSON file."
    
    # Limit rows if specified
    if max_rows:
        opportunities = opportunities[:max_rows]
    
    # Define columns
    columns = [
        ("Rank", 5),
        ("Score", 6),
        ("Title", 45),
        ("Source", 8),
        ("Category", 15),
        ("Pain", 5),
        ("Engage", 7),
        ("Recommendation", 20)
    ]
    
    headers = [col[0] for col in columns]
    widths = [col[1] for col in columns]
    
    # Build table
    output = []
    output.append(format_table_separator(widths, "top"))
    output.append(format_table_row(headers, widths))
    output.append(format_table_separator(widths, "middle"))
    
    for i, opp in enumerate(opportunities, 1):
        score = opp.get("opportunity_score", {})
        engagement = opp.get("engagement", {})
        
        row = [
            str(i),
            f"{score.get('total', 0):.1f}",
            opp.get("original_title", "No title")[:45],
            opp.get("source", "N/A"),
            opp.get("category", "N/A")[:15],
            f"{score.get('pain', 0):.0f}",
            f"{engagement.get('reactions', 0) + engagement.get('comments', 0)}",
            opp.get("recommendation", "")[:20]
        ]
        
        output.append(format_table_row(row, widths))
    
    output.append(format_table_separator(widths, "bottom"))
    
    return "\n".join(output)


def convert_keyword_summary_to_table(keyword_summary: Dict[str, Any]) -> str:
    """Convert keyword summary to table"""
    
    if not keyword_summary:
        return "No keyword summary found."
    
    columns = [
        ("Keyword", 40),
        ("Posts", 6),
        ("Problems", 9),
        ("Opps", 5),
        ("Top Score", 10)
    ]
    
    headers = [col[0] for col in columns]
    widths = [col[1] for col in columns]
    
    output = []
    output.append(format_table_separator(widths, "top"))
    output.append(format_table_row(headers, widths))
    output.append(format_table_separator(widths, "middle"))
    
    for keyword, data in keyword_summary.items():
        if "error" in data:
            row = [keyword[:40], "ERROR", "ERROR", "ERROR", "ERROR"]
        else:
            row = [
                keyword[:40],
                str(data.get("total_posts", 0)),
                str(data.get("problems_found", 0)),
                str(data.get("opportunities_found", 0)),
                f"{data.get('top_opportunity_score', 0):.1f}"
            ]
        
        output.append(format_table_row(row, widths))
    
    output.append(format_table_separator(widths, "bottom"))
    
    return "\n".join(output)


def convert_json_to_table(json_file: str, output_file: str = None, max_rows: int = None):
    """
    Main function to convert JSON research file to table format
    
    Args:
        json_file: Path to JSON file
        output_file: Optional output file (prints to console if not specified)
        max_rows: Limit number of opportunities shown
    """
    
    # Load JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return
    
    # Build output
    output = []
    output.append("=" * 120)
    output.append("📊 TORUKMACTO RESEARCH RESULTS")
    output.append("=" * 120)
    output.append("")
    
    # Add metadata
    if "research_completed_at" in data:
        output.append(f"Research completed: {data['research_completed_at']}")
        output.append(f"Total keywords: {data.get('total_keywords', 0)}")
        output.append(f"Total opportunities: {data.get('total_opportunities', 0)}")
        output.append("")
    elif "searched_at" in data:
        output.append(f"Search date: {data['searched_at']}")
        if "problem_keyword" in data:
            output.append(f"Keyword: {data['problem_keyword']}")
        output.append(f"Raw results: {data.get('raw_results', 0)}")
        output.append(f"Problems found: {data.get('problems_found', 0)}")
        output.append("")
    elif "scanned_at" in data:
        output.append(f"Scan date: {data['scanned_at']}")
        output.append(f"Tools scanned: {data.get('tools_scanned', 0)}")
        output.append(f"Total opportunities: {data.get('total_opportunities', 0)}")
        output.append("")
    
    # Show keyword summary if available
    if "keyword_summary" in data:
        output.append("")
        output.append("📋 KEYWORD SUMMARY")
        output.append("")
        output.append(convert_keyword_summary_to_table(data["keyword_summary"]))
        output.append("")
    
    # Show opportunities table
    output.append("")
    output.append("🎯 TOP OPPORTUNITIES")
    output.append("")
    
    opportunities = data.get("opportunities", [])
    if not opportunities:
        opportunities = data.get("top_opportunities", [])
    if not opportunities:
        opportunities = data.get("top_10_opportunities", [])
    if not opportunities:
        opportunities = data.get("all_opportunities", [])
    
    output.append(convert_opportunities_to_table(opportunities, max_rows))
    output.append("")
    output.append("=" * 120)
    
    result = "\n".join(output)
    
    # Output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✅ Table saved to: {output_file}")
    else:
        print(result)


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert TORUKMACTO JSON research files to readable tables"
    )
    parser.add_argument("json_file", help="Path to JSON file to convert")
    parser.add_argument("--output", "-o", help="Output file (optional, prints to console by default)")
    parser.add_argument("--max-rows", "-n", type=int, help="Limit number of rows shown")
    
    args = parser.parse_args()
    
    convert_json_to_table(args.json_file, args.output, args.max_rows)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python json_to_table.py <json_file> [--output file.txt] [--max-rows 20]")
        print("\nExamples:")
        print("  python json_to_table.py data/reddit_research_final_20260117.json")
        print("  python json_to_table.py data/full_scan_20260117.json --max-rows 10")
        print("  python json_to_table.py data/reddit_search_20260117.json -o results.txt")
        sys.exit(1)
    
    main()
