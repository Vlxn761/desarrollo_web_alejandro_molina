package app.tarea4.models;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class AvisoAdopcionResumido {
    private Integer id;
    private LocalDateTime fecha;
    private String sector;
    private String detalles;
    private String comuna;
    private String nota;

    public AvisoAdopcionResumido(AvisoAdopcion aviso) {
        String tipo;
        tipo = (aviso.getCantidad() > 1) ? aviso.getTipo() + 's' : aviso.getTipo();
        
        String unidadMedida = "año";
        if (aviso.getEdad() > 1) unidadMedida += 's';
        if (aviso.getUnidadMedida() == 'm'){
            unidadMedida = "mes";
            if (aviso.getEdad() > 1) unidadMedida += "es";
        }

        this.id = aviso.getId();
        this.fecha = aviso.getFechaIngreso();
        this.sector = aviso.getSector();
        this.detalles = aviso.getCantidad() + " " + tipo + " " + aviso.getEdad() + " " + unidadMedida;
        this.comuna = aviso.getComuna().getNombre();
        this.nota = aviso.getNota();
    }

    public Integer getId() {
        return id; 
    }
    public String getFecha(){
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        return fecha.format(formatter); 
    }
    public String getSector(){ 
        return sector; 
    }
    public String getDetalles(){ 
        return detalles; 
    }
    public String getComuna(){ 
        return comuna; 
    }
    public String getNota(){ 
        return nota; 
    }
}
