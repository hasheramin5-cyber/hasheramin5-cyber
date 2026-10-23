import json, os, re, urllib.request

USER = "hasheramin5-cyber"
TOKEN = os.environ["GH_TOKEN"]
TOTAL = 52  # line width used in the SVG layout


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    res = json.load(urllib.request.urlopen(req))
    if "errors" in res:
        raise SystemExit(res["errors"])
    return res["data"]["user"]


# contributions (last year), followers, public repo count
u = gql("""query($login:String!){user(login:$login){
  followers{totalCount}
  repositories(ownerAffiliations:OWNER, privacy:PUBLIC){totalCount}
  contributionsCollection{contributionCalendar{totalContributions}}}}""",
        {"login": USER})
contribs = u["contributionsCollection"]["contributionCalendar"]["totalContributions"]
followers = u["followers"]["totalCount"]
repos = u["repositories"]["totalCount"]

# total stars across public repos (paginated)
stars, cursor = 0, None
while True:
    r = gql("""query($login:String!,$after:String){user(login:$login){
      repositories(first:100, after:$after, ownerAffiliations:OWNER, privacy:PUBLIC){
        nodes{stargazerCount} pageInfo{hasNextPage endCursor}}}}""",
            {"login": USER, "after": cursor})["repositories"]
    stars += sum(n["stargazerCount"] for n in r["nodes"])
    if not r["pageInfo"]["hasNextPage"]:
        break
    cursor = r["pageInfo"]["endCursor"]

value = f"{contribs:,} last year"
dots = "." * max(2, TOTAL - 2 - len("Contributions:") - len(value) - 2)


def put(s, _id, text):
    return re.sub(rf'(id="{_id}">)[^<]*(</tspan>)', rf'\g<1>{text}\g<2>', s)


for f in ("dark_mode.svg", "light_mode.svg"):
    s = open(f, encoding="utf-8").read()
    s = put(s, "contrib_dots", f" {dots} ")
    s = put(s, "contrib_data", value)
    s = put(s, "repos_data", f"{repos:,}")
    s = put(s, "stars_data", f"{stars:,}")
    s = put(s, "followers_data", f"{followers:,}")
    open(f, "w", encoding="utf-8").write(s)
print("Updated:", value, repos, stars, followers)