package app.tarea4.models;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "aviso_adopcion")
public class AvisoAdopcion {

    @Id
    @SequenceGenerator(
            name = "aviso_adopcion_seq",
            sequenceName = "aviso_adopcion_seq",
            allocationSize = 1
    )
    @GeneratedValue(
            strategy = GenerationType.SEQUENCE,
            generator = "aviso_adopcion_seq"
    )
    private Integer id;

    @NotNull
    private LocalDateTime fechaIngreso;

    @ManyToOne
    @NotNull
    private Comuna comuna;

    private String sector;

    @NotNull
    private String nombre;

    private String email;

    private String celular;

    @NotNull
    private String tipo;

    @NotNull
    private Integer cantidad;

    @NotNull
    private Integer edad;

    @NotNull
    private Character unidadMedida;

    @NotNull
    private LocalDateTime fechaEntrega;

    private String descripcion;

    @OneToMany(mappedBy = "aviso")
    
    private List<Nota> notas;

    @Transient
    private String nota; 

    // No es necesario implementarlo para esta tarea
    public AvisoAdopcion() {
    }

    public Integer getId() {
        return id;
    }

    public LocalDateTime getFechaIngreso() {
        return fechaIngreso;
    }

    public Comuna getComuna() {
        return comuna;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getCelular() {
        return celular;
    }

    public String getTipo() {
        return tipo;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public Integer getEdad() {
        return edad;
    }

    public Character getUnidadMedida() {
        return unidadMedida;
    }

    public LocalDateTime getFechaEntrega() {
        return fechaEntrega;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public String getNota() {
        if (notas.isEmpty()) {
            return "-";
        }

        double promedio = notas.stream().mapToInt(Nota::getNota).average().getAsDouble();

        return String.format("%.2f", promedio);
    }
}
