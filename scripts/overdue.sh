#!/bin/sh
# SpecSelf per-tier overdue check (ADR-008 D11).
#
# Reads review filenames out of a reviews directory and prints one line per
# tier (weekly/monthly/quarterly/annual) whose newest recorded period is more
# than one period behind the current one. The period currently in progress is
# never overdue: a review one period behind "now" just hasn't been written
# yet. Prints nothing and exits 0 when every tier is current. This script
# only prints; it never writes a review.
#
# Usage: overdue.sh [reviews-dir]
#   default reviews-dir: ${CLAUDE_PROJECT_DIR:-.}/your-life/reviews

set -eu

dir="${1:-${CLAUDE_PROJECT_DIR:-.}/your-life/reviews}"

# ISO-week Monday epoch for year $1, week $2 (GNU date has no native ISO
# week-date parser, so derive it from Jan 4, which always falls in week 1).
week_epoch() {
    y="$1"; w="$2"
    j4_epoch=$(date -d "${y}-01-04" +%s)
    j4_dow=$(date -d "${y}-01-04" +%u)
    echo $(( j4_epoch - (j4_dow - 1) * 86400 + (10#$w - 1) * 7 * 86400 ))
}

weekly_latest=""; monthly_latest=""; quarterly_latest=""; annual_latest=""
found_any=0

for f in "$dir"/*; do
    [ -e "$f" ] || continue
    base=$(basename "$f")
    case "$base" in
        [0-9][0-9][0-9][0-9]-W[0-9][0-9]*)
            tok=$(printf '%s' "$base" | grep -oE '^[0-9]{4}-W[0-9]{2}' || true)
            [ -n "$tok" ] || continue
            found_any=1
            [ -z "$weekly_latest" ] || [ "$tok" \> "$weekly_latest" ] && weekly_latest="$tok"
            ;;
        [0-9][0-9][0-9][0-9]-Q[1-4]*)
            tok=$(printf '%s' "$base" | grep -oE '^[0-9]{4}-Q[1-4]' || true)
            [ -n "$tok" ] || continue
            found_any=1
            [ -z "$quarterly_latest" ] || [ "$tok" \> "$quarterly_latest" ] && quarterly_latest="$tok"
            ;;
        [0-9][0-9][0-9][0-9]-[0-9][0-9]*)
            tok=$(printf '%s' "$base" | grep -oE '^[0-9]{4}-(0[1-9]|1[0-2])' || true)
            [ -n "$tok" ] || continue
            found_any=1
            [ -z "$monthly_latest" ] || [ "$tok" \> "$monthly_latest" ] && monthly_latest="$tok"
            ;;
        [0-9][0-9][0-9][0-9]*)
            tok=$(printf '%s' "$base" | grep -oE '^[0-9]{4}' || true)
            [ -n "$tok" ] || continue
            found_any=1
            [ -z "$annual_latest" ] || [ "$tok" \> "$annual_latest" ] && annual_latest="$tok"
            ;;
    esac
done

# Persisted coherence reports (reviews/coherence/YYYY-MM-DD.md) live in a
# subdirectory, not among the tier reviews above. Track the newest one so its
# age can be surfaced below: a lapsed session opens with the last known state,
# not a blank slate (see steering/coherence.md, persistence and trend).
coherence_newest=""
cdir="$dir/coherence"
if [ -d "$cdir" ]; then
    for cf in "$cdir"/*.md; do
        [ -e "$cf" ] || continue
        cb=$(basename "$cf" .md)
        case "$cb" in
            [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])
                if [ -z "$coherence_newest" ] || [ "$cb" \> "$coherence_newest" ]; then
                    coherence_newest="$cb"
                fi
                ;;
        esac
    done
fi
if [ -n "$coherence_newest" ]; then found_any=1; fi

if [ "$found_any" -eq 0 ]; then
    echo "SpecSelf: no reviews yet — run GETTING-STARTED.md to seed your life OS."
    exit 0
fi

now_year=$(date +%Y)
now_month=$(date +%Y-%m)
now_gyear=$(date +%G)
now_w=$(date +%V)
now_week="${now_gyear}-W${now_w}"
now_mon10=$((10#$(date +%m)))
now_q=$(( (now_mon10 - 1) / 3 + 1 ))
now_quarter="${now_year}-Q${now_q}"

if [ -n "$weekly_latest" ]; then
    ly=$(printf '%s' "$weekly_latest" | cut -d'-' -f1)
    lw=$(printf '%s' "$weekly_latest" | cut -d'-' -f2 | sed 's/^W//')
    now_week_epoch=$(week_epoch "$now_gyear" "$now_w")
    latest_week_epoch=$(week_epoch "$ly" "$lw")
    diff=$(( (now_week_epoch - latest_week_epoch) / 604800 ))
    [ "$diff" -gt 1 ] && echo "SpecSelf: weekly review overdue (latest $weekly_latest, now $now_week)."
fi

if [ -n "$monthly_latest" ]; then
    ly=$(printf '%s' "$monthly_latest" | cut -d'-' -f1)
    lm=$(printf '%s' "$monthly_latest" | cut -d'-' -f2)
    now_idx=$(( 10#$now_year * 12 + now_mon10 ))
    latest_idx=$(( 10#$ly * 12 + 10#$lm ))
    diff=$(( now_idx - latest_idx ))
    [ "$diff" -gt 1 ] && echo "SpecSelf: monthly review overdue (latest $monthly_latest, now $now_month)."
fi

if [ -n "$quarterly_latest" ]; then
    ly=$(printf '%s' "$quarterly_latest" | cut -d'-' -f1)
    lq=$(printf '%s' "$quarterly_latest" | cut -d'-' -f2 | sed 's/^Q//')
    now_idx=$(( 10#$now_year * 4 + now_q ))
    latest_idx=$(( 10#$ly * 4 + 10#$lq ))
    diff=$(( now_idx - latest_idx ))
    [ "$diff" -gt 1 ] && echo "SpecSelf: quarterly review overdue (latest $quarterly_latest, now $now_quarter)."
fi

if [ -n "$annual_latest" ]; then
    diff=$(( 10#$now_year - 10#$annual_latest ))
    [ "$diff" -gt 1 ] && echo "SpecSelf: annual review overdue (latest $annual_latest, now $now_year)."
fi

if [ -n "$coherence_newest" ]; then
    newest_epoch=$(date -d "$coherence_newest" +%s)
    now_epoch=$(date +%s)
    age_days=$(( (now_epoch - newest_epoch) / 86400 ))
    if [ "$age_days" -gt 7 ]; then
        echo "SpecSelf: latest coherence report is ${age_days}d old ($coherence_newest); run /weekly to refresh it."
    fi
fi

exit 0
