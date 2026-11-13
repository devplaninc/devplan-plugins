## How to estimate

Estimate from the team's git history in Devplan, not from ideal hours. Use the last 90 days and leave bots out (authors ending in `[bot]`, dependabot, renovate). Timestamps are epoch milliseconds; write the computed number in place of `$since`.

1. **Team pace from git.**
   ```
   MATCH (a:Person)-[:AUTHORED]->(pr:PullRequest)
   WHERE pr.mergedAt >= $since AND NOT coalesce(a.name,'') ENDS WITH '[bot]'
   RETURN count(DISTINCT a) AS engineers, count(DISTINCT pr) AS prs,
     percentileCont((pr.mergedAt - pr.openedAt)/3600000.0, 0.5) AS p50_hours,
     percentileCont((pr.mergedAt - pr.openedAt)/3600000.0, 0.85) AS p85_hours
   ```
   PRs per engineer-week = prs ÷ engineers ÷ weeks in the window.
2. **PRs per project, from comparable work.** Count the PRs behind each project's linked changes. Recent changes often link to commits rather than PRs, so count both, and convert commits to PRs with the workspace's ratio of merged PRs to commits over the same window (close to 1 when the team squash-merges).
   ```
   MATCH (c:Change)-[:LINKED_TO]->(p:Project) WHERE c.periodEnd >= $since
   MATCH (c)-[:USED]->(x) WHERE x:PullRequest OR x:GitCommit
   RETURN p.projectId,
     count(DISTINCT CASE WHEN x:PullRequest THEN x END) AS prs,
     count(DISTINCT CASE WHEN x:GitCommit THEN x END) AS commits
   ORDER BY prs + commits DESC LIMIT 50
   ```
   Join project IDs to `list_workspace_projects` for titles. Pick the 2 or 3 projects closest in area and scope as comparables.
3. **PRs this work needs.** Break the scope into pieces (from the technical approach, or the project's description), estimate PRs for each piece from the comparables, and add them up as a low-high range. For work already in progress, subtract the PRs already linked to it.
4. **Convert to time.**
   - Effort in engineer-weeks = PRs ÷ PRs per engineer-week.
   - Calendar time = the larger of (effort ÷ engineers on it) and (the longest chain of PRs that must land one after another × p85 cycle time).
   - Plan on the low PR count and median pace. Use the high PR count and p85 cycle time as the risk case.
5. **Show the basis in one line,** for example: "Based on 410 PRs from 4 engineers over 90 days (8 PRs per engineer-week; cycle time 0.9 hours median, 41 hours at p85). Comparable projects took 28 to 40 PRs."

Never invent precision. With no comparable project, give a wide range and say what would narrow it.
