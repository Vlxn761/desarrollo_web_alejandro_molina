package app.tarea4.controllers;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;

import app.tarea4.models.AvisoAdopcionResumido;
import app.tarea4.models.Eval;

import app.tarea4.services.AppService;

@Controller
public class AppController {
    private final AppService appService;
    public AppController(AppService appService) {
        this.appService = appService;
    }
    
    @GetMapping("/")
    public String listadoAdopciones(@RequestParam(defaultValue="0") int page, Model model) {
        Page<AvisoAdopcionResumido> modelData = appService.getAvisosData(page, 5);
        model.addAttribute("data", modelData);
        return "base";
    }

    
    @PostMapping("/post-nota")
    public ResponseEntity<String> postNotaRoute(@RequestBody Eval nota) throws Exception {
        appService.handlePostRequest(nota.getId(), nota.getNota());

        return ResponseEntity.ok("OK"); 
    }
}
