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
    const speakOutput = 'Welcome to grocery gather, how can I help?';
    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();
  }
};


//adding functionality for adding food items to grocery gather's memory
const AddFoodIntentHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.intent.name === 'AddFoodIntent';
  },

  handle(handlerInput) {
    //const checkFoodOutput = 'Adding your items to the cart.';
    const food = handlerInput.requestEnvelope.request.intent.slots.food.value;
    const count = handlerInput.requestEnvelope.request.intent.slots.count.value;
    const meal = handlerInput.requestEnvelope.request.intent.slots.meal.value;

    const speakOutput = `Thanks, I'll remember that you ate ${count} ${food} at ${meal}.`;

    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();
  }
};

// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.
exports.handler = Alexa.SkillBuilders.custom()
  .addRequestHandlers(
    LaunchRequestHandler,
    AddFoodIntentHandler)
  .lambda();
