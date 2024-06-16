payload = """
// https://stackoverflow.com/questions/3115982/how-to-check-if-two-arrays-are-equal-with-javascript
function arraysEqual(a, b) {
  if (a === b) return true;
  if (a == null || b == null) return false;
  if (a.length !== b.length) return false;

  for (var i = 0; i < a.length; ++i) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

function main() {
    let socket = new WebSocket("ws://localhost:8764");
    var toCompare = "";

    socket.onopen = function(e) {
        console.log("[LOG] sending client ping")
        socket.send("client ping");
    }

    socket.onclose = function(e) {
        setTimeout(function() {
          main();
        }, 1000);
    }

    socket.onmessage = function(e) {
        var message = JSON.parse(e.data);

        console.log(message.message)
        if (message.message === "clear") {
            console.log("[LOG] removing expressions from the graph");
            Calc.getExpressions().map((i) => {
                return i.id;
                console.log(`[LOG] removing expression ${i.id}`);
            }).map((i) => {
                Calc.removeExpression({ id: i });
            });
        } else if (message.message === "expression") {
            console.log(`[LOG] adding expression ${message.payload} as id ${message.id}`);
            Calc.setExpression({
                type: "expression",
                latex: message.payload,
                id: message.id,
            })
        } else if (message.message === "ticker") {
            var state = Calc.getState();

            state.expressions.ticker = {
                handlerLatex: message.payload,
                minStepLatex: message.rate,
                open: true,
            };

            Calc.setState(JSON.stringify(state))
        } else if (message.message === "eval") {
            toCompare = eval(message.expectedOutput);
            var exp = Calc.HelperExpression({
                latex: message.expression
            })
            var timeoutid = setTimeout(function() {
                console.log("[LOG] failing because timeout occured")
                socket.send(JSON.stringify({
                    "name": message.expression,
                    "output": "false"
                }))
                exp.unobserve('listValue')
            }, 5000);
            exp.observe('listValue', function () {
                console.log(exp.listValue);
                if(arraysEqual(exp.listValue, toCompare)) {
                    socket.send(JSON.stringify({
                        "name": message.expression,
                        "output": "true"
                    }))
                    clearTimeout(timeoutid);
                }
            })
            Calc.controller.listModel.ticker.playing = true;
        } else {
            console.log(`[LOG] couldn't parse message ${e.data}`)
        }
    }
} main();
"""
