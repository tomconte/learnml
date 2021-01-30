import React from "react";
import "./style.css";

class TopicApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      textAreaValue: ""
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  render() {
    return (
      <div>
        <h3>Topic Score</h3>
        <form onSubmit={this.handleSubmit}>
          <label htmlFor="score-text">Enter text to be scored.</label>
          <textarea
            value={this.state.textAreaValue}
            id="text"
            onChange={this.handleChange}
          />
          <button>Score</button>
        </form>
      </div>
    );
  }

  handleChange(e) {
    this.setState({ textAreaValue: e.target.value });
  }

  handleSubmit(e) {
    e.preventDefault();
    console.log(this.state.textAreaValue);

    fetch("https://fmtmcustom.azurewebsites.net/api/score", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        data: this.state.textAreaValue
      })
    })
      .then(response => response.text())
      .then(response => {
        console.log(response);
      })
      .catch(err => {
        console.log("fetch failed");
        console.log(err);
      });
  }
}

export default TopicApp;
