import re

from flask import Flask, render_template, request

from search import Search

app = Flask(__name__)

es = Search()


def extract_filters(query):
    filters = []

    filter_regex = r"category:([^\s]+)\s*"
    m = re.search(filter_regex, query)

    if m:
        filters.append({"term": {"category.keyword": {"value": m.group(1)}}})
        query = re.sub(filter_regex, "", query).strip()

    filter_regex = r"year:([^\s]+)\s*"
    m = re.search(filter_regex, query)
    if m:
        filters.append(
            {
                "range": {
                    "updated_at": {
                        "gte": f"{m.group(1)}||/y",
                        "lte": f"{m.group(1)}||/y",
                    }
                }
            }
        )
        query = re.sub(filter_regex, "", query).strip()
    return {"filter": filters}, query


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/")
def handle_search():
    query = request.form.get("query", "")
    filters, parsed_query = extract_filters(query)
    from_ = request.form.get("from_", type=int, default=0)
    results = es.search(
        query={
            "bool": {
                "must": {
                    "multi_match": {
                        "query": parsed_query,
                        "fields": ["name", "summary", "content"],
                    }
                },
                **filters,
            }
        },
        size=5,
        from_=from_,
    )
    return render_template(
        "index.html",
        query=query,
        results=results["hits"]["hits"],
        from_=0,
        total=results["hits"]["total"]["value"],
    )


@app.get("/document/<id>")
def get_document(id):
    document = es.retrieve_document(id)
    title = document["_source"]["name"]
    paragraphs = document["_source"]["content"].split("\n")
    return render_template("document.html", title=title, paragraphs=paragraphs)


@app.cli.command()
def reindex():
    """Regenerate the Elasticsearch index."""
    response = es.reindex()
    print(
        f"Index with {len(response["items"])} documents created in {response["took"]} milliseconds."
    )
