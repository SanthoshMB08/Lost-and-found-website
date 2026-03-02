package com.dev.LAF.controllers;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;


@RestController
@RequestMapping("/api/laf/v1/search")
public class SearchController {
    @GetMapping("/search-lost")
    public String searchLost(@RequestParam String param) {
        return new String();
    }
    @GetMapping("/search-founds")
    public String searchFounds(@RequestParam String param) {
        return new String();
    }
    @GetMapping("/search-users")
    public String searchUsers(@RequestParam String param) {
        return new String();
    }
    @GetMapping("/search-random")
    public String searchRandom(@RequestParam String param) {
        return new String();
    }
}
