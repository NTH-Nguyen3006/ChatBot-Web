from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

@app.route("/", methods = ["GET"])
def home():
    return render_template("home.html")

@app.route("/introduction", methods = ["GET"])
def introduction():
    return render_template("introduction.html")

@app.route("/bot", methods = ["POST"])
def botController():
    
    
    return jsonify({
        "model": r"""
Chào bạn! Tôi là một trợ lý ảo.
Đây là một **tin nhắn mẫu** với _một vài_ định dạng.
Bạn có thể thấy hiệu ứng gõ chữ của tôi.

`Đây là một đoạn code inline`

Đây là một khối code:

```CS
public static void Main() {
    Console.Writeline("Hello World!");
}
```

Cảm ơn bạn đã theo dõi!
"""
    }), 200



if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)