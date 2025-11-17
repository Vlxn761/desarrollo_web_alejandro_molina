package app.tarea4.services;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;


import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;

import app.tarea4.models.AvisoAdopcion;
import app.tarea4.models.AvisoAdopcionRepository;
import app.tarea4.models.AvisoAdopcionResumido;
import app.tarea4.models.Nota;
import app.tarea4.models.NotaRepository;

@Service
public class AppService {

    private final String pathStatic;
    private final AvisoAdopcionRepository avisoAdopcionRepository;
    private final NotaRepository notaRepository;

    public AppService(AvisoAdopcionRepository avisoAdopcionRepository, 
                    NotaRepository notaRepository) throws IOException {
        this.avisoAdopcionRepository = avisoAdopcionRepository;
        this.notaRepository = notaRepository;

        // Dynamically resolve the absolute path for the static directory
        Path staticDir = Paths.get(ResourceUtils.getFile("classpath:static").getAbsolutePath());
        this.pathStatic = staticDir.toString();
        System.out.println("Static path resolved to: " + this.pathStatic);
    }

    public Page<AvisoAdopcionResumido> getAvisosData(Integer page, Integer pageSize) {
        Page<AvisoAdopcion> avisosData = avisoAdopcionRepository.findAll(PageRequest.of(page, pageSize));
        return avisosData.map(AvisoAdopcionResumido::new);
    }

    public AvisoAdopcion getAvisoById(Integer id) {
        AvisoAdopcion aviso = avisoAdopcionRepository.findById(id).get();
        return aviso;
    }

    public void handlePostRequest(Integer id, Integer nota) throws Exception {
        if (nota >= 1 && nota <= 7) {
            AvisoAdopcion aviso = getAvisoById(id);
            Nota notaDato = new Nota(aviso, nota); 
            notaRepository.save(notaDato);
            System.out.println("Nota guardada exitosamente.");
        } else {
            throw new IllegalArgumentException("Validación de nota fallida.");
        }
    }
}
