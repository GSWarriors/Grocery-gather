
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
        var speakOutput = "";
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        if (sessionAttributes.visits === 0) {
          speakOutput = 'Welcome to grocery gather, what items are in your shopping cart? You can say up to 1.'
        } else {
          var numItems = sessionAttributes.pastItems.length;
          speakOutput = `Welcome back to grocery gather, you currently have ${numItems} items in your shopping cart.
          Please say the items you would like to add.`
        }


        // increment the number of visits and save the session attributes so the
        // ResponseInterceptor will save it persistently.
        sessionAttributes.visits += 1;
        handlerInput.attributesManager.setSessionAttributes(sessionAttributes);


        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};

//then, invocation goes to next step- one of the intents based on what the user said in response
//note: this is equivalent to PlayGameHandler

const AddShoppingCartHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
          && handlerInput.requestEnvelope.request.intent.name === 'AddShoppingCartIntent';
    },

    handle(handlerInput) {

        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();
        var speakOutput = '';
        const firstItem = handlerInput.requestEnvelope.request.intent.slots.first_item.value;


        if (sessionAttributes.firstItem === null) {

          speakOutput = `Thanks, I'll remember that you added ${firstItem} as your item for the week.`;
          sessionAttributes.firstItem = firstItem;

          //save the session attributes
          handlerInput.attributesManager.setSessionAttributes(sessionAttributes);

          //add item to list of past items?
          sessionAttributes.pastItems.push(sessionAttributes.firstItem);

          return handlerInput.responseBuilder
              .speak(speakOutput)
              .getResponse();
        } else {


          speakOutput = `You already have an item added.`

          return handlerInput.responseBuilder
              .speak(speakOutput)
              .getResponse();
        }


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
// It will simply repeat the intent the user said.
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


//request interceptors run before handlers are run (canHandle) functions
// get persistent attributes, using await to ensure the data has been returned before
// continuing execution
const LoadDataInterceptor = {
  async process(handlerInput) {
    const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

    var persistent = await handlerInput.attributesManager.getPersistentAttributes();
    if (!persistent) persistent = {};

    //here, we initialize the variables for items we send in so that its easier to work
    //with them in the handlers- specifically addshoppingcarthandler in this case.
    if(!sessionAttributes.hasOwnProperty('firstItem')) sessionAttributes.firstItem = null;

    if(!persistent.hasOwnProperty('pastItems')) persistent.pastItems = [];
    if(!sessionAttributes.hasOwnProperty('pastItems')) sessionAttributes.pastItems = [];

    //change the below
    // if you're tracking pastItems between sessions, use the persistent value
    // set the visits value (either 0 for new, or the persistent value)
    sessionAttributes.pastItems = (item_tracking) ? persistent.pastItems : sessionAttributes.pastItems;
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


// Response Interceptors run after all skill handlers complete, before the response is
// sent to the Alexa servers.
const SaveDataInterceptor = {

    async process(handlerInput) {
        const persistent = {};
        const sessionAttributes = handlerInput.attributesManager.getSessionAttributes();

        //save past items and visits
        persistent.pastItems = (item_tracking) ? sessionAttributes.pastItems : [];
        persistent.visits = sessionAttributes.visits;

        //set and save persistent attributes
        handlerInput.attributesManager.setPersistentAttributes(persistent);
        let waiter = await handlerInput.attributesManager.savePersistentAttributes();
    }
};


// This response interceptor will log all outgoing responses of this lambda
const LoggingResponseInterceptor = {
    process(handlerInput, response) {
        console.log('----- RESPONSE -----');
        console.log(JSON.stringify(response, null, 2));
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
