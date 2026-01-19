package main

import (
	"encoding/json"
	"errors"
	"log"
	"net/http"

	"github.com/IBM/sarama"
)

type TableMessage struct {
	Table   string   `json:"table"`
	Columns []string `json:"columns"`
	Rows    [][]any  `json:"rows"`
}

func (m *TableMessage) Validate() error {
	if m.Table == "" {
		return errors.New("table name is empty")
	}
	if len(m.Columns) == 0 {
		return errors.New("columns are empty")
	}
	if len(m.Rows) == 0 {
		return errors.New("rows are empty")
	}

	for _, row := range m.Rows {
		if len(row) != len(m.Columns) {
			return errors.New("row length does not match columns count")
		}
	}

	return nil
}

type KafkaProducer struct {
	producer sarama.SyncProducer
	topic    string
}

func NewKafkaProducer(brokers []string, topic string) (*KafkaProducer, error) {
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true
	config.Producer.RequiredAcks = sarama.WaitForAll

	p, err := sarama.NewSyncProducer(brokers, config)
	if err != nil {
		return nil, err
	}

	return &KafkaProducer{
		producer: p,
		topic:    topic,
	}, nil
}

func (kp *KafkaProducer) Send(msg TableMessage) error {
	bytes, err := json.Marshal(msg)
	if err != nil {
		return err
	}

	message := &sarama.ProducerMessage{
		Topic: kp.topic,
		Value: sarama.ByteEncoder(bytes),
	}

	_, _, err = kp.producer.SendMessage(message)
	return err
}

func sendHandler(kp *KafkaProducer) http.HandlerFunc { //http handler
	return func(w http.ResponseWriter, r *http.Request) {
		var msg TableMessage

		if err := json.NewDecoder(r.Body).Decode(&msg); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		if err := msg.Validate(); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		if err := kp.Send(msg); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Message sent to Kafka"))
	}
}

func main() { //Kafka has to be started here
	brokers := []string{"10.23.29.182:9092"}
	topic := "etl-topic"

	kafkaProducer, err := NewKafkaProducer(brokers, topic)
	if err != nil {
		log.Fatal(err)
	}

	http.HandleFunc("/send", sendHandler(kafkaProducer))

	log.Println("Producer started")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
