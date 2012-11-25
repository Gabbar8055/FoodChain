﻿// Utility functions


// Force Enyo to process ondragover event
document.ondragover = enyo.dispatch;


// Namespace
FoodChain = {};

// Game context handling
FoodChain.context = {
	score: 0,
	game: "",
	level: 0
};
FoodChain.saveContext = function() {
	FoodChain.sugar.sendMessage(
		"save-context", {
			score: FoodChain.context.score,
			game: FoodChain.context.game,
			level: FoodChain.context.level
	});
};
FoodChain.loadContext = function(context) {
	if (context.score) FoodChain.context.score = parseInt(context.score);
	if (context.game) FoodChain.context.game = context.game;
	if (context.level) FoodChain.context.level = parseInt(context.level);
};

// Global config, HACK: put it in a dummy rule of the CSS file
FoodChain.getConfig = function(name) {
	// Description of config parameters
	var config = [
		{ name: "screen-width", attribute: "width", strip: 2},
		{ name: "screen-height", attribute: "height", strip: 2},
		{ name: "card-width", attribute: "margin-left", strip: 2}
	];
	
	// Look for the parameter
	for (var i = 0 ; i < config.length ; i++ ) {
		// Same name
		if (config[i].name == name) {
			// Get value in the style
			var el = document.getElementById("header");
			var value = null;
			if (el.currentStyle) {
				value = el.currentStyle[config[i].attribute];
			} else if (window.getComputedStyle) {
				value = document.defaultView.getComputedStyle(el,null).getPropertyValue(config[i].attribute);
			}
			
			// Strip value
			if (value != null) {
				value = 10*value.substring(0, value.length-config[i].strip)
			}
			return value;
		}
	}
	return null;
};

// Home handling
FoodChain.goHome = function() {
	if (FoodChain.context.home != null) {
		FoodChain.context.game = "";
		FoodChain.context.home.renderInto(document.getElementById("body"));
	}
};

// Sugar interface
FoodChain.sugar = new Sugar();
FoodChain.sugar.connect("localization", __$FC_l10n_set);
FoodChain.sugar.connect("save-context", FoodChain.saveContext);
FoodChain.sugar.connect("load-context", FoodChain.loadContext);
FoodChain.log = function(msg) {
	FoodChain.sugar.sendMessage("console-message", msg);
	console.log(msg);
};

// Add and remove a class to an element
FoodChain.addRemoveClass = function(element, toAdd, toRemove) {
	element.removeClass(toRemove);
	element.addClass(toAdd);
};

// "Old style" sleep function
FoodChain.sleep = function(delay) {
	var start = new Date().getTime();
	while (new Date().getTime() < start + delay);
};

// Create a object respecting a condition on a set of object
FoodChain.createWithCondition = function(create, condition, set) {
	var conditionValue;
	var newObject;
	var time = 0;
	do {
		conditionValue = true;
		newObject = create();
		for (var i = 0; conditionValue && i < set.length ; i++) {
			conditionValue = condition(newObject, set[i]);
		}
		time++;
	} while (!conditionValue && time < 12); // time to avoid infinite or too long loop in very complex situation
	if (!conditionValue)
		FoodChain.log("WARNING: out of pre-requisite creating "+newObject.id);
	return newObject;
};
