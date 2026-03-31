from pydantic import BaseModel, ValidationError
from typing import Type, TypeVar, Generic, Dict, Any
from struttura.strutturaResult import Result, display_errore

T = TypeVar('T', bound=BaseModel)


class Builder(Generic[T]):
    def __init__(self, model_cls: Type[T]):
        if not issubclass(model_cls, BaseModel):
            risultato = Result.failure("model_cls deve essere una sottoclasse di pydantic.Basemodel")
            display_errore(risultato)
            raise

        self._model_cls = model_cls
        self.dati_builder: Dict[str, Any] = {}

    def _set(self, key: str, value: Any) -> "Builder[T]":
        self.dati_builder[key] = value
        return self

    def costruisci(self) -> Result:
        try:
            modello_validato = self._model_cls(**self.dati_builder)
            return Result.success(modello_validato)
        except ValidationError as e:

            errori_puliti = []

            for error in e.errors():
                nome_campo = error.get('loc', ('campo sconosciuto',))[0]
                messaggio = error.get('msg', 'Errore non specificato')
                valore_errato = error.get('input')

                errori_puliti.append(f"\n- Campo '{nome_campo}': {messaggio}. (Valore fornito: '{valore_errato}')")

            info_errore_formattato = "".join(errori_puliti)

            risultato = Result.failure(f"Errore durante la costruzione di '{self._model_cls.__name__}'", info=info_errore_formattato)
            # display_errore(risultato)
            # raise
            return risultato


def generate_setters_for(model: Type[BaseModel]):
    """
    Un decoratore che ispeziona un modello Pydantic e genera automaticamente
    i metodi set_* per una classe Builder.
    """

    def decorator(builder_class):
        # Itera su tutti i nomi dei campi definiti nel modello Pydantic
        for field_name in model.model_fields.keys():
            setter_name = f"set_{field_name}"

            # Definiamo una funzione "setter" specifica per questo campo
            # Usiamo un trucco con un argomento di default (name=field_name)
            # per "catturare" il valore corretto di field_name in ogni iterazione del ciclo.
            def setter_method(self, value, name=field_name):
                return self._set(name, value)

            # Aggiungiamo il metodo appena creato alla classe Builder
            setattr(builder_class, setter_name, setter_method)

        return builder_class

    return decorator


def generate_getters_for(model: Type[BaseModel], data_attribute_name: str):
    """
    Un decoratore che genera automaticamente delle property in stile get_*
    per ogni campo di un modello Pydantic.

    Args:
        model: Il modello Pydantic da ispezionare.
        data_attribute_name: Il nome della variabile di istanza che contiene
                             l'oggetto del modello Pydantic (es. "_dati").
    """
    def decorator(target_class):
        # Itera su tutti i nomi dei campi definiti nel modello Pydantic
        for field_name in model.model_fields.keys():
            getter_name = f"get_{field_name}"

            # Definiamo la funzione getter che verrà usata dalla property.
            # Usiamo di nuovo il trucco dell'argomento di default per "catturare"
            # il valore corretto di field_name.
            def getter_method(self, name=field_name):
                # Prende l'istanza del modello Pydantic (es. self._dati)
                data_model_instance = getattr(self, data_attribute_name)
                # Restituisce il valore dell'attributo richiesto da quell'istanza
                return getattr(data_model_instance, name)

            # Crea l'oggetto property usando la nostra funzione come getter
            getter_property = property(getter_method)

            # Aggiunge la property appena creata alla classe target (es. RecordC1)
            setattr(target_class, getter_name, getter_property)

        return target_class
    return decorator