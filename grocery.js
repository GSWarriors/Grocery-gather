//
// Alexa Fact Skill - Sample for Beginners
//

'use strict'
// sets up dependencies
const Alexa = require('ask-sdk-core');



// core functionality for fact skill
const LaunchRequestHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
  },

  handle(handlerInput) {
    const speakOutput = 'Welcome to grocery gather, what items would you like to enter?';
    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();
  }

};

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
  .addRequestHandlers(LaunchRequestHandler)
  .lambda();




/*
'Product_ValueControlIntent': function() {

},

'AMAZON_NUMBER_ValueControlIntent': function() {

},

'AMAZON_DATE_ValueControlIntent': function() {

},

'CheckFoodIntent': function() {

},

//triggered when user wants to add food to cart
'AddFoodIntent': function() {
  this.emit(':tell', 'Hello')
}*/






  //'AddProductIntent': function() {
    //triggered when use wants to add food to cart

    //tell- one way
    //this.emit(':tell', 'Hello')

    //another way to do same thing
    //this.response.speak('Hello').cardRenderer('Title', 'Body text')
    //this.emit(':responseReady')


    //asks. Asks again if user doesn't say anything
    //this.emit(':ask', 'How can I help?', 'You can say something like...')

    //another way to do same thing
    //this.response.speak('How can i Help?').listen('You can say something like...')
    //this.emit(':responseReady')
  //}
