package com.dev.LAF.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController
@RequestMapping("/api/laf/v1/feed")
public class FeedController {

    @GetMapping("/filter-feed")
    public String filterFeed(@RequestParam String param) {
        return new String();
    }
    
    
}
