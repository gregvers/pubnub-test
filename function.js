export default (request) => {
    const kvstore = require('kvstore');
    const xhr = require('xhr');

    console.log('request',request); // Log the request envelope passed
    if (request.message.msg == "caca") {
        console.log('bad word',request.message.msg);
        request.message.msg = "####"
    }
    return request.ok(); // Return a promise when you're done
}