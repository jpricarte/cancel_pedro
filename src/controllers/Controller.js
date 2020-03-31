const connection = require('../database/connection');

module.exports = {
    //Add a new cancel on db
    async newCancel (request, response) {
        const { user, app, time } = request.body;

        //printing infos, for debug
        console.log(user);
        console.log(app);
        console.log(time);
        
        //adding a new cancel on database
        const [id] = await connection('cancelamentos').insert({
            user,
            app,
            time
        });
        
        //returning what was added
        return response.json({
            "status": "sucess",
            "id": id,
            "user": user,
            "app": app,
            "time": time
        });
    },

    //Return all cancels
    async index(request, response)
    {
        const cancel = await connection('cancelamentos').select('*');
    
        return response.json(cancel);
    }
}