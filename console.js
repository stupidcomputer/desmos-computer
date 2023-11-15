function main() {
    let socket = new WebSocket("ws://localhost:8765");
    var ids = [];

    socket.onopen = function(e) {
        socket.send("client ping");
    }

    socket.onmessage = function(e) {
        var message = JSON.parse(e.data);

        console.log(message.message)
        if (message.message === "clear") {
            for(i in ids) {
                console.log("removing")
                Calc.removeExpression({
                    id: ids[i],
                })
            }

            ids = [];
        } else if (message.message === "expression") {
            Calc.setExpression({
                type: "expression",
                latex: message.payload,
                id: message.id,
            })
            ids.push(message.id)
            console.log(ids)
        } else if (message.message === "ticker") {
            var state = Calc.getState();
            
            state.expressions.ticker = {
                handlerLatex: message.payload,
                minStepLatex: message.rate,
                open: true,
            };

            Calc.setState(JSON.stringify(state))
        } else {
            console.log("unknown message type.")
        }

        console.log(message);
    }
}