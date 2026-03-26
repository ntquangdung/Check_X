from flask import Flask, jsonify, render_template, request

from checker import BatchChecker


app = Flask(__name__)
checker = BatchChecker()


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/check")
def check_usernames():
    payload = request.get_json(silent=True) or {}
    raw_usernames = payload.get("usernames", "")

    if not isinstance(raw_usernames, str):
        return jsonify({"error": "Danh sach username khong hop le."}), 400

    usernames = []
    for line in raw_usernames.replace(",", "\n").splitlines():
        cleaned = line.strip().lstrip("@")
        if cleaned and cleaned not in usernames:
            usernames.append(cleaned)

    if not usernames:
        return jsonify({"error": "Ban chua nhap username nao."}), 400

    results = checker.check_many(usernames)
    summary = {
        "total": len(results),
        "live": sum(1 for item in results if item["status"] == "live"),
        "suspended": sum(1 for item in results if item["status"] == "suspended"),
        "die": sum(1 for item in results if item["status"] == "die"),
    }
    return jsonify({"results": results, "summary": summary})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
