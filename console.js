function main() {
    let socket = new WebSocket("ws://localhost:8764");
    var ids = [];

    socket.onopen = function(e) {
        console.log("[LOG] sending client ping")
        socket.send("client ping");
    }

    socket.onmessage = function(e) {
        var message = JSON.parse(e.data);

        console.log(message.message)
        if (message.message === "clear") {
            console.log("[LOG] removing expressions from the graph");
            for(i in ids) {
                console.log(`[LOG] removing expression ${ids[i]}`)
                Calc.removeExpression({
                    id: ids[i],
                })
            }

            ids = [];
        } else if (message.message === "expression") {
            console.log(`[LOG] adding expression ${message.payload} as id ${message.id}`);
            Calc.setExpression({
                type: "expression",
                latex: message.payload,
                id: message.id,
            })
            ids.push(message.id)
        } else if (message.message === "ticker") {
            var state = Calc.getState();
            
            state.expressions.ticker = {
                handlerLatex: message.payload,
                minStepLatex: message.rate,
                open: true,
            };

            Calc.setState(JSON.stringify(state))
        } else {
            console.log(`[LOG] couldn't parse message ${e.data}`)
        }
    }
} main();
