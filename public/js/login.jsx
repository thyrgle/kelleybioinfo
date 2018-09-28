import React from 'react';

class LogIn extends React.Component {
  constructor(props) {
    super(props);
  }

  onLogIn() {
  }

  render() {
    return (
      <div>
        <input type="text" name="username" id="username"/>
        <input type="text" name="password" id="password"/>
        <button className="login" onclick={this.onLogin}>
          Log In
        </button>
      </div>
    )
  }
}
