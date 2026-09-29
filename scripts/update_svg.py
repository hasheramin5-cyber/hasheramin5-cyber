import json, os, re, urllib.request

USER = "hasheramin5-cyber"
TOKEN = os.environ["GH_TOKEN"]
TOTAL = 52  # line width used in the SVG layout

query = """query($login:String!){user(login:$login){contributionsCollection{
contributionCalendar{totalContributions}}}}"""
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
)
data = json.load(urllib.request.urlopen(req))
count = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

value = f"{count:,} last year"
dots = "." * max(2, TOTAL - 2 - len("Contributions:") - len(value) - 2)

for f in ("dark_mode.svg", "light_mode.svg"):
    s = open(f, encoding="utf-8").read()
    s = re.sub(r'(id="contrib_dots">)[^<]*(</tspan>)', rf'\g<1> {dots} \g<2>', s)
    s = re.sub(r'(id="contrib_data">)[^<]*(</tspan>)', rf'\g<1>{value}\g<2>', s)
    open(f, "w", encoding="utf-8").write(s)
print("Updated:", value)