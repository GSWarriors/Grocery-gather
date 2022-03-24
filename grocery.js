
const Alexa = require('ask-sdk-core');
const AWS = require('aws-sdk')
const ddbAdapter = require('ask-sdk-dynamodb-persistence-adapter')

//tracking past items between sessions? yes
const item_tracking = true;



const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    handle(handlerInput) {
        //const speakOutput = 'Welcome to grocery gather, how can I help?';
        const speakOutput = 'Welcome to grocery gather, what items are in your shopping cart? You can say up to 5.'

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};

//then, invocation goes to next step- one of the intents based on what the user said in response

const AddShoppingCartHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
          && handlerInput.requestEnvelope.request.intent.name === 'AddShoppingCartIntent';
    },

    handle(handlerInput) {
        const firstItem = handlerInput.requestEnvelope.request.intent.slots.first_item.value;
        const secondItem = handlerInput.requestEnvelope.request.intent.slots.second_item.value;
        const thirdItem = handlerInput.requestEnvelope.request.intent.slots.third_item.value;
        const fourthItem = handlerInput.requestEnvelope.request.intent.slots.fourth_item.value;
        const fifthItem = handlerInput.requestEnvelope.request.intent.slots.fifth_item.value;

        const speakOutput = `Thanks, I'll remember that you added ${firstItem} ${secondItem}
        ${thirdItem} ${fourthItem} and ${fifthItem} as your items for the week.`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();

    }
};






const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        // Any cleanup logic goes here.
        return handlerInput.responseBuilder.getResponse();
    }
};

// The intent reflector is used for interaction model testing and debugging.
// It will simply repeat the intent the user said. You can create custom handlers
// for your intents by defining them above, then also adding them to the request
// handler chain below.
const IntentReflectorHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest';
    },
    handle(handlerInput) {
        const intentName = handlerInput.requestEnvelope.request.intent.name;
        const speakOutput = `You just triggered ${intentName}`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            //.reprompt('add a reprompt if you want to keep the session open for the user to respond')
            .getResponse();
    }
};

// Generic error handling to capture any syntax or routing errors. If you receive an error
// stating the request handler chain is not found, you have not implemented a handler for
// the intent being invoked or included it in the skill builder below.
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`~~~~ Error handled: ${error.message}`);
        const speakOutput = `Sorry, I couldn't understand what you said. Please try again.`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};


//add request interceptors code here
const LoadDataInterceptor = {
  async process(handlerInput) {
    const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

    // get persistent attributes, using await to ensure the data has been returned before
    // continuing execution

    var persistent = await handlerInput.attributesManager.getPersistentAttributes();
    if (!persistent) persistent = {};


    //here, we initialize the variables for items we send in so that its easier to work
    //with them in the handlers- specifically addshoppingcarthandler in this case.
    if(!sessionAttributes.hasOwnProperty('firstItem')) sessionAttributes.firstItem = null;

    if(!persistent.hasOwnProperty('pastItems')) persistent.pastItems = [];
    if(!sessionAttributes.hasOwnProperty('pastItems')) sessionAttributes.pastItems = [];

    //change the below
    // if you're tracking past_celebs between sessions, use the persistent value
    // set the visits value (either 0 for new, or the persistent value)
    sessionAttributes.past_celebs = (celeb_tracking) ? persistent.past_celebs : sessionAttributes.past_celebs;
    sessionAttributes.visits = (persistent.hasOwnProperty('visits')) ? persistent.visits : 0;

    //set the session attributes so they're available to your handlers
    handlerInput.attributesManager.setSessionAttributes(sessionAttributes);
      }
  };
  // This request interceptor will log all incoming requests of this lambda
  const LoggingRequestInterceptor = {
      process(handlerInput) {
          console.log('----- REQUEST -----');
          console.log(JSON.stringify(handlerInput.requestEnvelope, null, 2));
      }
  };







// The SkillBuilder acts as the entry point for your skill, routing all request and response
// payloads to the handlers above. Make sure any new handlers or interceptors you've
// defined are included below. The order matters - they're processed top to bottom.

//register 2 request and response interceptors.
//before running req handlers, the req interceptors run
//after handler returns result, the resp. interceptors run
exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        AddShoppingCartHandler,
        //AddFoodIntentHandler,
        SessionEndedRequestHandler,
        IntentReflectorHandler) // make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
    .addRequestInterceptors(
        LoadDataInterceptor,
        LoggingRequestInterceptor
    )
    .addResponseInterceptors(
      SaveDataInterceptor,
      LoggingResponseInterceptor
    )


    .addErrorHandlers(
        ErrorHandler)
    .withPersistenceAdapter(
      new ddbAdapter.DynamoDbPersistenceAdapter({
        tableName: process.env.DYNAMODB_PERSISTENCE_TABLE_NAME,
        createTable: false,
        dynamoDBClient: new AWS.DynamoDB({apiVersion: 'latest', region: process.env.DYNAMODB_PERSISTENCE_REGION})
      })
    )
    .lambda();
