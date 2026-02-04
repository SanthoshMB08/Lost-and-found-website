package com.lostandfound.project.newproject.controllers;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController
public class FeedController {
    @GetMapping("/getfeed")
    public String getMethodName(@RequestParam String location) {
        return "Feed for location: " + location;
    }
    
    

    
}
