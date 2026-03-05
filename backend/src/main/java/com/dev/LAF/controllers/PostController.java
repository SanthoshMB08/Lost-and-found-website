package com.dev.LAF.controllers;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
@RestController
@RequestMapping("/api/laf/v1/posts")
public class PostController {
    
    @PostMapping("/create")
    public String createLost() {
        return "post created successfully!";
    }
 
    @PutMapping("/update")
    public String updateLost(@PathVariable Long id) {
        return "post updated successfully!";
    }
  
    @PutMapping("/found-claim")
    public String claimFound( @RequestBody String entity) {
        
        return entity;
    }
    @PutMapping("/lost-claim")
    public String claimLost(@PathVariable String id, @RequestBody String entity) {
        
        return entity;
    }
    @PutMapping("/update-claim")
    public String updateClaim(@RequestBody String entity) {
        
        return entity;
    }
    @GetMapping("/get-claim")
    public String getClaim(@RequestParam String param) {
        return new String();
    }
   
}
